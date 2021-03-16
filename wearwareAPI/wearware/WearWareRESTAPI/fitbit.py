import base64
import datetime
import json
import logging
from urllib.parse import urlsplit, urlencode, urlunsplit

import requests
from django.conf import settings
from django.core.mail import mail_managers, send_mail
from django.core.exceptions import ValidationError
from django.db import transaction
from django.template import loader, Context
from django.utils import timezone
from pytz import timezone as pytz_tz

from .models import FitbitAccount, SyncRecord, FitbitMinuteRecord, FitbitHeartRecord, FitbitSleepRecord

fitbit_auth_url = 'https://www.fitbit.com/oauth2/authorize'
fitbit_token_url = 'https://api.fitbit.com/oauth2/token'

log = logging.getLogger(__name__)


def fitbit_build_auth_url(subject):
    params = {
        'client_id': '22DGBB',
        'response_type': 'code',
        'scope': 'activity heartrate location settings sleep profile',
        'state': str(subject.pk) + ' ' + subject.pairing_token.hex,
    }
    url_parts = list(urlsplit(fitbit_auth_url))
    url_parts[3] = urlencode(params)
    auth_url = urlunsplit(url_parts)
    return auth_url


def fitbit_build_request_headers(device=None):
    if device is None:
        fitbit_auth_blob = '22DGBB' + ':' + '36408b69aa9977c4f991b4255ac16af7'
        fitbit_auth_blob = fitbit_auth_blob.encode('utf8')
        auth_header = 'Basic ' + base64.b64encode(fitbit_auth_blob).decode('utf8')

    else:
        auth_header = device.token_type + ' ' + device.access_token

    headers = {
        'Authorization': auth_header,
        'Accept-Locale': 'en_US',
        'Accept-Language': 'en_US',
    }
    return headers


def fitbit_fetch_permanent_token(temp_token):
    headers = fitbit_build_request_headers()

    payload = {
        'code': temp_token,
        'grant_type': 'authorization_code',
        'client_id': settings.FITBIT_CLIENT_ID
    }

    r = requests.post(fitbit_token_url, data=payload, headers=headers)
    if not r.ok:
        log.error('Unable to fetch permanent token (%s): %s', r.status_code, r.text)
        r.raise_for_status()

    auth_info = json.loads(r.text)
    return auth_info


reauthorization_template = loader.get_template('fitbit_reauthorize_email.txt')


def fitbit_refresh_access_token(device):
    headers = fitbit_build_request_headers()

    payload = {
        'grant_type': 'refresh_token',
        'refresh_token': device.refresh_token,
    }

    log.info('Requesting fresh auth token for device_id %s.', device.pk)
    r = requests.post(fitbit_token_url, data=payload, headers=headers)
    if not r.ok:
        log.error('Unable to refresh auth token for device %s:\n%s',
                  device.pk, r.text)

        error_info = json.loads(r.text)
        invalid_token = 'invalid_grant' in [
            e['errorType'] for e in error_info['errors']]

        if invalid_token:
            failed_refresh = SyncRecord.objects.create(device=device,
                                        start_time=timezone.now(),
                                        end_time=timezone.now(),
                                        sync_type='fitbit-token-refresh',
                                        successful=False,
                                        message='Failed refreshing token for device. '
                                                'Request:{}\n{}\n{}\n'
                                                'Response:\n{}\n{}'.format(
                                                fitbit_token_url, headers, payload,
                                                r.headers, r.text))

            # TODO dynamically insert server address FIXME
            context = Context(
                {'device': device, 'pairing_token': device.subject.pairing_token})
            email_body = reauthorization_template.render(context)

            try:
                send_mail('WearWare - Reauthorization Needed', email_body, settings.DEFAULT_FROM_EMAIL,
                          [device.subject.email])

                email_body = """{}\'s auth refresh failed. Email sent to their registered address.
                Request:
                {} {}\n{}\n{}
                Response:
                {} {}:{}\n{}\n{}\n{}
                Fitbit account:
                {}, {}, {}, {}, {}, {}
                """.format(
                        device.subject.identifier,
                        r.request.method, r.request.url, r.request.headers, r.request.body,
                        r.elapsed, r.status_code, r.url, r.headers, r.text, r.cookies,
                        device.identifier, device.subject.identifier, device.last_updated, device.token_type,
                        device.refresh_token,
                        device.access_token)
                mail_managers('WearWare - Subject auth refresh failed', email_body, fail_silently=True)

                log.warning(
                        'Sent email requesting reauthorization to %s for fibit account %s.',
                        device.subject.email,
                        device.identifier)
            except:
                log.error('Unable to send email to %s for fitbit reauthorization.', device.subject.email)

            log.error('Disabling device %s due to invalid refresh token.', device.identifier)
            device.is_active = False
            device.save()
        return

    auth_info = json.loads(r.text)
    auth_info.pop('scope')
    auth_info.pop('expires_in')

    device.token_type = auth_info['token_type']
    device.access_token = auth_info['access_token']
    device.refresh_token = auth_info['refresh_token']
    device.is_active = True
    device.save()

    refresh_sync = SyncRecord.objects.create(
        device=device,
        start_time=timezone.now(),
        end_time=timezone.now(),
        sync_type='fitbit-token-refresh',
        successful=True,
        message='Succeeded refreshing token for device.'
        )

    log.info('Successfully updated authentication info for fitbit %s.',
             device.identifier)


def fitbit_start_subscription(device):
    headers = fitbit_build_request_headers(device)
    requests.post('https://api.fitbit.com/1/user/-/activities/apiSubscriptions/{}.json'.format(device.subject.pk),
                  headers=headers)

    log.info('Registered fitbit subscription for device %s.', device.pk)


def fitbit_end_subscription(device_id):
    device = FitbitAccount.objects.get(pk=device_id)
    headers = fitbit_build_request_headers(device)

    # get list of active subscriptions for user
    r = requests.get(
        'https://api.fitbit.com/1/user/-/activities/apiSubscriptions.json', headers=headers)

    if not r.ok:
        log.error('Problem deleting subscription for fibit account %s: %s',
                  device.identifier, r.text)
        return

    subs = json.loads(r.text).get('apiSubscriptions', [])

    # delete all active subscriptions
    for sub in subs:
        try:
            sub_id = sub['subscriptionId']
            url = 'https://api.fitbit.com/1/user/-/activities/apiSubscriptions/{}.json'.format(
                sub_id)
            r = requests.delete(url, headers=headers)
            r.raise_for_status()

            log.info('Deleted subscription for device %s.', device.pk)
        except KeyError:
            pass


@transaction.atomic
def fitbit_make_request(url, device_id):
    device = FitbitAccount.objects.select_for_update().get(pk=device_id)
    headers = fitbit_build_request_headers(device)

    r = requests.get(url, headers=headers)
    if not r.ok:
        log.error('Received error from response: %s, response headers:\n%s\nresponse body:\n%s',
                  r.status_code,
                  r.headers,
                  r.text)
        r.raise_for_status()
    log.info('Made GET request to %s, status %s', url, r.status_code)
    log.debug('Response:\n%s', r.text)
    return r


def fitbit_build_activity_request_url(activity_type, end_time, start_time):
    if activity_type == "sleep":
        update_url = "https://api.fitbit.com/1/user/-/sleep/date/{start_year}-{start_month}-{start_day}.json"
        url_params = {
            'start_year': '{:04d}'.format(start_time.year),
            'start_month': '{:02d}'.format(start_time.month),
            'start_day': '{:02d}'.format(start_time.day)
        }   
    else:
        update_url = 'https://api.fitbit.com/1/user/-/activities/{activity_type}/date/' \
                    '{start_year}-{start_month}-{start_day}/1d/{resolution}/' \
                    'time/{start_hour}:{start_minute}/{end_hour}:{end_minute}.json'
        url_params = {
            'activity_type': activity_type,
            'start_year': '{:04d}'.format(start_time.year),
            'start_month': '{:02d}'.format(start_time.month),
            'start_day': '{:02d}'.format(start_time.day),
            'start_hour': '{:02d}'.format(start_time.hour),
            'start_minute': '{:02d}'.format(start_time.minute),
            'end_hour': '{:02d}'.format(end_time.hour),
            'end_minute': '{:02d}'.format(end_time.minute),
            'resolution': '1sec' if activity_type == 'heart' else '1min',
        }
    url = update_url.format(**url_params)
    return url


def fitbit_fetch_fresh_data(device, start, end, activities):
    time_tuples_to_query = segment_time_range_at_midnight(start, end)
    last_good_time = None
    remaining_calls = 20
    for start_time, end_time in time_tuples_to_query:
        log.warning("START: %s\nEND: %s", start_time, end_time)
        if remaining_calls < 20:
            log.warning(
                'Getting close to rate limit of fitbit API calls for {}. Stopping for now.'.format(
                    device.identifier))
            break

        activity_data = {}
        for activity_type in activities:

            url = fitbit_build_activity_request_url(
                activity_type, end_time, start_time)
            r = fitbit_make_request(url, device_id=device.pk)

            record_sync_type = 'fitbit-{}'.format(activity_type)
            if r.ok:
                activity_data[activity_type] = r.text
                sync_record = SyncRecord.objects.create(device=device, sync_type=record_sync_type,
                                         start_time=start_time, end_time=end_time,
                                         message='Fetched fitbit account {}\'s {} data from {} to {}.'.format(
                                                 device.identifier,
                                                 activity_type,
                                                 start_time,
                                                 end_time))

                last_good_time = end_time
                remaining_calls = int(r.headers['Fitbit-Rate-Limit-Remaining'])

            else:
                log.debug(r.text)
                log.error(
                    'Unable to fetch activity data for account %s!', device.identifier)

                sync_record = SyncRecord.objects.create(device=device, successful=False, sync_type=record_sync_type,
                                         start_time=start_time, end_time=end_time,
                                         message='Failed fetching fitbit account {}\' {} data from {} to {}. '
                                                 'Error message: {}'.format(
                                                     device.identifier,
                                                     activities,
                                                     start_time,
                                                     end_time, r.text))
        fitbit_parse_and_persist_activity_data(
            device.identifier, activity_data)
    return last_good_time


def fitbit_parse_and_persist_activity_data(owner_id, activities):
    try:
        device = FitbitAccount.objects.filter(
            identifier=owner_id).order_by('-is_active').first()
    except FitbitAccount.DoesNotExist:
        log.warning(
            'Asked to update data for device %s, but it\' doesn\'t exist! Skipping.', owner_id)
        return

    if not device.is_active:
        log.warning(
            'Asked to update data for device %s, but it\'s marked as inactive. Skipping.', owner_id)
        return

    to_persist = {}

    for activity in activities:
        container = json.loads(activities[activity])
        if activity != 'sleep':
            metadata_header = 'activities-{}'.format(activity)
            data_header = metadata_header + '-intraday'

            date_string = container[metadata_header][0]['dateTime']
            dataset = container[data_header]['dataset']

            for datum in dataset:
                timestamp = date_string + ' ' + datum['time']
                seconds = int(timestamp[-2:])
                timestamp = timestamp[:-2] + '00'
                if timestamp not in to_persist:
                    to_persist[timestamp] = {}

                if activity == 'steps':
                    to_persist[timestamp]['steps'] = int(datum['value'])

                elif activity == 'distance':
                    to_persist[timestamp]['distance'] = float(datum['value'])

                elif activity == 'calories':
                    calories = float(datum['value'])
                    mets = float(datum['mets']) / 10

                    if calories == 0.0 and mets == 0.0:
                        continue

                    to_persist[timestamp]['calories'] = calories
                    to_persist[timestamp]['mets'] = mets
                    to_persist[timestamp]['fb_level'] = int(datum['level'])

                elif activity == 'heart':
                    if 'heart' not in to_persist[timestamp]:
                        to_persist[timestamp]['heart'] = []

                    to_persist[timestamp]['heart'].append(
                        (seconds, datum['value']))

        else:
            if not 'sleep' in container:
                container['sleep'] = {}
            
            tmp_container = container['sleep']

            if len(tmp_container) > 0:
                for num in range(len(container) - 1):
                    tmp_record = tmp_container[num]
                    date = tmp_record['dateOfSleep']
                    summary = container['summary']
                    stages = summary['stages']

                    if date not in to_persist:
                        to_persist[date] = {}
                        to_persist[date][num] = {}
                    
                    to_persist[date][num]['deepSleep'] = stages['deep']
                    to_persist[date][num]['lightSleep'] = stages['light']
                    to_persist[date][num]['remSleep'] = stages['rem']
                    to_persist[date][num]['awake'] = stages['wake']
                    to_persist[date][num]['totalAsleep'] = summary['totalMinutesAsleep']
                    to_persist[date][num]['inBed'] = summary['totalTimeInBed']


    for timestamp in to_persist:
        if len(timestamp) <= 10:
            naive_dt = naive_dt = datetime.datetime.strptime(timestamp, '%Y-%m-%d')
        else:
            naive_dt = datetime.datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')
        aware_dt = pytz_tz(device.timezone).localize(naive_dt)
        utc = pytz_tz('UTC')

        datum = to_persist[timestamp]

        if 'steps' in datum:
            if 'calories' not in datum and 'mets' not in datum:
                if datum['steps'] == 0:
                    continue

        try:
            # let's see if we already have a record for this minute
            record = FitbitMinuteRecord.objects.get(
                device=device, timestamp=aware_dt.astimezone(utc))

            # if we've made it this far, there's no exception and the record exists
            # get the existing data for this minute

            # only insert new data, never overwrite existing data
            if record.steps is None:
                record.steps = datum.get('steps')

            if record.calories is None:
                record.calories = datum.get('calories')

            if record.mets is None:
                record.mets = datum.get('mets')

            if record.activity_level is None:
                record.activity_level = datum.get('fb_level')

            if record.distance is None:
                record.distance = datum.get('distance')

            if 'heart' in datum:
                hr_records = datum['heart']
                for hr_record in hr_records:
                    FitbitHeartRecord.objects.create(
                        FitbitAccount=record, 
                        second=hr_record[0], 
                        bpm=hr_record[1],
                        timestamp=hr_record[2]
                        )

            record.save()

        except FitbitMinuteRecord.DoesNotExist:
            record = FitbitMinuteRecord.objects.create(
                device=device,
                timestamp=aware_dt,
                steps=datum.get(
                    'steps'),
                calories=datum.get(
                    'calories'),
                mets=datum.get('mets'),
                activity_level=datum.get(
                    'fb_level'),
                distance=datum.get('distance')
                )

            if 'heart' in datum:
                hr_records = datum['heart']
                for hr_record in hr_records:
                    FitbitHeartRecord.objects.create(
                        FitbitAccount=record,
                        second=hr_record[0],
                        bpm=hr_record[1],
                        timestamp=hr_record[2]
                    )

        except FitbitMinuteRecord.MultipleObjectsReturned:
            # this shouldn't ever happen as long as this function is the only way used to insert fitbit data
            log.error(
                'There are duplicate records for device %s at timestamp %s. Not updating.', device.pk, aware_dt)
            continue

        if 0 in datum:
            ## get fitbit sleep record
            for record_number in datum:
                sleep_record = datum[record_number]
                try:
                    sleep = FitbitSleepRecord.objects.filter(record_number=num, timestamp=timestamp)

                    if len(sleep) > 0:
                        sleep.update(deep_sleep_minutes=sleep_record['deepSleep'])
                        sleep.update(light_sleep_minutes=sleep_record['lightSleep'])
                        sleep.update(rem_sleep_minutes=sleep_record['remSleep'])
                        sleep.update(awake_minutes=sleep_record['awake'])
                        sleep.update(total_sleep_minutes=sleep_record['totalAsleep'])
                        sleep.update(time_in_bed=sleep_record['inBed'])

                    else:
                        deep_sleep_minutes = sleep_record['deepSleep']
                        light_sleep_minutes = sleep_record['lightSleep']
                        rem_sleep_minutes = sleep_record['remSleep']
                        awake_minutes = sleep_record['awake']
                        total_sleep_minutes = sleep_record['totalAsleep']
                        time_in_bed = sleep_record['inBed']
                        
                        sleep = FitbitSleepRecord.objects.create(
                            device=device,
                            timestamp=timestamp,
                            record_number=record_number,
                            deep_sleep_minutes=deep_sleep_minutes,
                            light_sleep_minutes=light_sleep_minutes,
                            rem_sleep_minutes=rem_sleep_minutes,
                            awake_minutes=awake_minutes,
                            total_sleep_minutes=total_sleep_minutes,
                            time_in_bed=time_in_bed
                        )

                except FitbitSleepRecord.DoesNotExist:
                    for record_number in datum:
                        sleep_record = datum[record_number]

                        deep_sleep_minutes = sleep_record['deepSleep']
                        light_sleep_minutes = sleep_record['lightSleep']
                        rem_sleep_minutes = sleep_record['remSleep']
                        awake_minutes = sleep_record['awake']
                        total_sleep_minutes = sleep_record['totalAsleep']
                        time_in_bed = sleep_record['inBed']

                        sleep = FitbitSleepRecord.objects.create(
                            device=device,
                            timestamp=timestamp,
                            record_number=record_number,
                            deep_sleep_minutes=deep_sleep_minutes,
                            light_sleep_minutes=light_sleep_minutes,
                            rem_sleep_minutes=rem_sleep_minutes,
                            awake_minutes=awake_minutes,
                            total_sleep_minutes=total_sleep_minutes,
                            time_in_bed=time_in_bed
                        )

def segment_time_range_at_midnight(begin, end):
    time_range_tuples = []
    segment_begin = begin
    segment_end = datetime.datetime(segment_begin.year, segment_begin.month, segment_begin.day, 23, 59, 0, 0,
                                    tzinfo=begin.tzinfo)

    for _ in range(7):
        if segment_end != end:
            time_range_tuples.append((segment_begin, segment_end))
            segment_begin = segment_end + datetime.timedelta(minutes=1)
            segment_end += datetime.timedelta(days=1)

    time_range_tuples.append((segment_begin, segment_end))

    return time_range_tuples
