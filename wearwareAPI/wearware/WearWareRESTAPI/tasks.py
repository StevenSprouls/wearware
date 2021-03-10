import sys
import datetime
import requests
from __future__ import absolute_import
from celery import shared_task
from django.utils import timezone
from pytz import timezone as pytz_tz
from django.core.mail import send_mail, mail_managers
from django.db import transaction
import dateutil.parser
from urllib.parse import urlsplit, urlencode, urlunsplit
from wearware.fitbit import * # -- this is what jensen is working on 
from WearWareRESTAPI.models import *


@shared_task
@transaction.atomic
def fitbit_refresh_tokens():
    #Scheduled task to refresh Fitbit authentication tokens.
    for device in FitbitAccount.objects.select_for_update().filter(is_active=True):
        fitbit_refresh_access_token(device)


@shared_task
@transaction.atomic
def fitbit_update_activity_data(owner_id):
    #Fetch up to date activity data for a given Fitbit account.
    try:
        # very important that this select_for_update happens in a @transaction.atomic
        # to prevent multiple notifications running in sync and clobbering a user's records
        device = FitbitAccount.objects.select_for_update().get(identifier=owner_id)

        if not device.is_active:
            log.warning('Asked to update data for device %s, but it\'s marked as inactive. Skipping.', owner_id)
            return

        # save the notification before we do anything else
        notification_record = SyncRecord(device=FitbitAccount.objects.get(identifier=owner_id),
                                         start_time=timezone.now(),
                                         end_time=timezone.now(),
                                         sync_type='fitbit-notification',
                                         successful=True,
                                         message='Received valid fitbit notification '
                                                 'for device {}'.format(owner_id))
        notification_record.save()

    except FitbitAccount.DoesNotExist:
        log.warning('Asked to update data for device %s, but it\' doesn\'t exist! Skipping.', owner_id)
        return

    # start figuring out how far back our updates need to go
    subject_tz = pytz_tz(device.timezone)
    now_in_subject_tz = timezone.now().astimezone(subject_tz)  # - datetime.timedelta(minutes=5)
    last_updated = device.last_updated.astimezone(subject_tz)

    # find the previous successful sync and update the heartrate data
    try:
        previous_hr_sync_time = SyncRecord.objects.filter(
            successful=True, device=device, sync_type='fitbit-steps') \
            .order_by('-start_time')[1].timestamp.astimezone(subject_tz)

        previous_hr_sync_time -= datetime.timedelta(minutes=5)

        log.info('Attempting to backfill fitbit heartrate data for %s from %s to %s.', device.identifier,
                 previous_hr_sync_time, last_updated)
        fitbit_fetch_fresh_data(device, previous_hr_sync_time, last_updated, ['heart'])
    except IndexError:
        pass

    if last_updated >= now_in_subject_tz:
        return

    # try to get the rest of the data
    last_good_fetch = fitbit_fetch_fresh_data(device, last_updated, now_in_subject_tz,
                                              ['calories', 'steps', 'distance', 'heart'])

    if last_good_fetch is not None:
        device.last_updated = last_good_fetch - datetime.timedelta(minutes=3)
        device.save()

def inactive_participant_action():
    #Check for inactive participants and send out a notification
    inactive_participants = []
    message = "We noticed inactivity from your fitbit device. Please being wearing your fitbit again " \
               "or contact your study administrator if there is an issue with your device. Thank you."
    log.info('Checking all participants for inactivity')
    for participant in Participant.objects.all():
        for device in FitbitAccount.objects.filter(participant=participant):
            sync_record = SyncRecord.objects.filter(device=device)
            last_sync = sync_record.timestamp
            six_hours_before = datetime.now() - timedelta(hours=6)
            if last_sync <= six_hours_before:
                inactive_participants.append(participant.email, participant.phone)
    log.info('Found {} inactive participants'.format(len(inactive_participant)))
    for participant in inactive_participants:
        log.info('Sending inactivity message to email {}'.format(participant[0]))
        emailpeople(message, participant[0])

def emailpeople(message, emails):
    subject = "WearWare Study Message"
    body = """You have received a message from a researcher from WearWare!
            The message is as follows: {message}""".format(message=message)
    send_from = "wearware.test@gmail.com"
    log.info("Begin sending email(s) with message '%s' to %s", message, emails)
    send_mail(
        subject,
        body,
        send_from,
        emails
    )
    log.info("Finished sending email(s)")
