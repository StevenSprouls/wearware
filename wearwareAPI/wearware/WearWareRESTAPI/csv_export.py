import csv
import io
import os
import logging
from zipfile import ZipFile, ZIP_DEFLATED

from django.db.models import F
from django.forms.models import model_to_dict
from django.utils import timezone
from django.utils.text import slugify
from django.core.mail import EmailMessage
from django.contrib.auth.models import User

from background_task import background

from .models import *

log = logging.getLogger(__name__)

@background(schedule=1)
def create_zip_export_bytes(study_id, researcher_id, start_date, end_date):
    study = Study.objects.get(pk=study_id)
    researcher = User.objects.get(pk=researcher_id)

    activity_types = [
        'steps',
        'calories',
        'mets',
        'fb_level',
        'distance',
        'heart',
        'sleep'
    ]

    buffer = io.BytesIO()
    earliest = None
    latest = None

    with ZipFile(buffer, mode='w', compression=ZIP_DEFLATED) as zip:
        for study_participant in StudyHasParticipant.objects.filter(study=study):
            subject = study_participant.participant

            try:
                device = FitbitAccount.objects.get(subject=subject)
            except FitbitAccount.DoesNotExist:
                continue

            device_tz = timezone.pytz.timezone(device.timezone)

            # get all of the records for this subject's device
            records = FitbitMinuteRecord.objects.filter(device=device, timestamp__gte=start_date, timestamp__lte=end_date)
            hr_records = FitbitHeartRecord.objects.filter(minute_record__device=device).annotate(
                timestamp=F('minute_record__timestamp'))
            sleep_records = FitbitSleepRecord.objects.filter(device=device, timestamp__gte=start_date, timestamp__lte=end_date)

            if len(records) == 0:
                continue

            # find out if we have records for this subject before or after records for other subjects
            first_timestamp = records.first().timestamp.astimezone(device_tz)
            if earliest is None or earliest > first_timestamp:
                earliest = first_timestamp

            last_timestamp = records.last().timestamp.astimezone(device_tz)
            if latest is None or latest < last_timestamp:
                latest = last_timestamp

            # parse the JSON data from each DB record and sort them all by timestamp
            data = {}
            sleep_data = {}

            for r in records:
                data[r.timestamp] = {
                    'steps': r.steps,
                    'calories': r.calories,
                    'mets': r.mets,
                    'fb_level': r.activity_level,
                    'distance': r.distance
                }

            for r in hr_records:
                if r.timestamp in data:
                    if 'heart' not in data[r.timestamp]:
                        data[r.timestamp]['heart'] = []
                    data[r.timestamp]['heart'].append((r.second, r.bpm))
            
            sleep_fields = [
                'record_number',
                'deep_sleep_minutes',
                'light_sleep_minutes',
                'rem_sleep_minutes',
                'awake_minutes',
                'total_sleep_minutes',
                'time_in_bed'
                ]

            for r in sleep_records:
                tmp_dict = model_to_dict(r)
                if r.timestamp not in sleep_data:
                    sleep_data[r.timestamp] = {}
                    tmp_data = sleep_data[r.timestamp]
                for field in sleep_fields:
                    tmp_data[field] = tmp_dict[field]
                
            sorted_data = sorted([(t.astimezone(device_tz), d) for t, d in data.items()])
            sorted_sleep = sorted([(t, d) for t, d in sleep_data.items()])

            for activity in activity_types:

                # this is a relative path to within the zip file
                filename = ('fitbit_{field}' + os.sep +
                            '{study}_{subject}_fitbit_{field}_{start_date}_{end_date}.csv').format(
                    study=slugify(study.name),
                    subject=slugify(subject.pk),
                    field=slugify(activity),
                    start_date=first_timestamp.strftime('%Y%m%d'),
                    end_date=last_timestamp.strftime('%Y%m%d'),
                )

                # again, write CSV contents to memory -- this could change if it gets too big
                file = io.StringIO()
                csv_out = csv.writer(file)
                
                if activity == 'sleep':

                    #CSV header
                    csv_out.writerow(
                        ['year', 'month', 'day', 'record_number', 'deep_sleep', 'light_sleep', 'rem_sleep', 'awake', 'total', 'in_bed']
                    )

                    for timestamp, datum in sorted_sleep:
                        year, month, day = timestamp.strftime('%Y %m %d').split()
                        tmp_fields = []
                        tmp_fields.append(year)
                        tmp_fields.append(month)
                        tmp_fields.append(day)
                        for field in sleep_fields:
                            tmp_fields.append(datum[field])
                        csv_out.writerow(tmp_fields)
                else:
                    # CSV header
                    csv_out.writerow(
                        ['year', 'month', 'day', 'hour', 'minute', 'second', 'microsecond', activity])

                    for timestamp, datum in sorted_data:
                        if activity in datum:
                            # each row needs the time data first
                            year, month, day, hour, minute, second, microsecond = timestamp.strftime(
                                '%Y %m %d %H %M %S %f').split()

                            # because HR data is at a higher frequency, each datum should write multiple rows
                            if activity == 'heart':
                                for tick, value in datum[activity]:
                                    second = '{:02d}'.format(tick)
                                    csv_out.writerow(
                                        [year, month, day, hour, minute, second, microsecond, value]
                                        )
                            else:
                                csv_out.writerow(
                                    [year, month, day, hour, minute, second, microsecond, datum[activity]]
                                    )                     


                # add our CSV data to the zip file at the relative path we specified
                zip.writestr(filename, file.getvalue().encode('utf8'))

    # we'll need to tell the caller what these bytes should be saved as
    zip_filename_template = '{study}_{start}_{end}.zip'
    zip_filename = zip_filename_template.format(study=slugify(study.name),
                                                start=earliest.strftime(
                                                    '%Y%m%d'),
                                                end=latest.strftime('%Y%m%d'))

    # f_disk = open('/opt/wwcsvs/'+zip_filename, 'wb')
    # f_disk.write(buffer)
    # f_disk.close()
    email = EmailMessage(
        "WearWare Study Data",
        "Attached to this email is the data for the study named {study}".format(study=study.name),
        "sms968@nau.edu", #my email for testing, dont fuck with it
        [researcher.email]
    )

    email.attach(zip_filename, buffer.getvalue(), 'application/zip')

    email.send()

    return zip_filename, buffer
