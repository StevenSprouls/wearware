import hmac
import pprint
import socket
import statistics
import os
import re
import csv
import codecs
import phonenumbers
import subprocess
from django.forms.models import model_to_dict
from django.utils import timezone
from django.core.files import File
from django.contrib.auth.models import Group,User
from django.core.exceptions import PermissionDenied
from django.db.models import Count, Q
from django.http import HttpResponseServerError, HttpResponse, HttpResponseBadRequest, Http404
from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.views.decorators.csrf import csrf_exempt
from datetime import timedelta
from guardian.shortcuts import get_objects_for_user, assign_perm, remove_perm
from ipware.ip import get_real_ip
from dateutil.parser import parse
from .csv_export import *
from .fitbit import *
from .forms import *
from .models import FitbitAccount, Study, Participant
from .tasks import *
from subprocess import Popen, PIPE

log = logging.getLogger(__name__)

def fitbit_init_auth(request, subject_id):
    subject = get_object_or_404(Participant, pk=subject_id)

    try:
        pairing_token = uuid.UUID(request.GET['token'])
    except:
        raise PermissionDenied

    if pairing_token != subject.pairing_token:
        raise PermissionDenied

    auth_url = fitbit_build_auth_url(subject)
    log.info('Initiating Fitbit pairing process for subject: %s.', subject.pk)
    return render(request, 'fitbit/fitbit_auth_init.html', context={'auth_url': auth_url, 'subject': subject})


def fitbit_initial_oauth_callback(request):
    profile_url = 'https://api.fitbit.com/1/user/-/profile.json'

    received_params = request.GET
    if 'error' in received_params:
        log.error('Fitbit passed back error (%s) in OAuth callback.', received_params['error'])
        return HttpResponseServerError('Received error from Fitbit: {}'.format(received_params['error']))

    state = received_params['state'].split(' ')

    try:
        if len(state) != 2:  # there should be a subject ID and a pairing token, no more no less
            raise ValueError('Invalid number of state arguments received!')

        subject_id = int(state[0])

        subject = get_object_or_404(Participant, pk=subject_id)
        token = uuid.UUID(hex=state[1])
        print(token, subject.pairing_token)
        if token != subject.pairing_token:
            raise ValueError('Invalid pairing token for subject {}!'.format(subject.email))

        subject.pairing_token = uuid.uuid4()
        subject.save()

    except ValueError as e:
        log.warning('Unable to complete OAuth pairing process (from %s): %s', get_real_ip(request), e)
        raise PermissionDenied

    temp_token = received_params['code']

    auth_info = fitbit_fetch_permanent_token(temp_token)

    participant_studies = StudyHasParticipant.objects.filter(participant=subject)

    device = FitbitAccount(
        subject=subject,
        token_type=auth_info['token_type'],
        access_token=auth_info['access_token'],
        refresh_token=auth_info['refresh_token'],
        is_active=True,
        identifier=''
        )

    log.info(
        'Successfully obtained authentication info for subject {}\'s fitbit with id {}.'.format(subject_id,
                                                                                                device.pk))

    headers = {
        'Authorization': (auth_info['token_type'] + ' ' + auth_info['access_token']),
        'Accept-Locale': 'en_US',
        'Accept-Language': 'en_US',
    }

    r = requests.get(profile_url, headers=headers)

    if not r.ok:
        log.error('Received error from response: %s, response body:\n%s', r.status_code, r.text)
        return HttpResponseServerError('Unable to collect needed profile information.')

    profile = json.loads(r.text)['user']

    for exclude in ('avatar', 'avatar150', 'topBadges'):
        if exclude in profile:
            profile.pop(exclude)

    device.identifier = profile['encodedId']
    # check for duplicate identifiers and delete device if it exists
    try:
        # old refresh token expires as soon as new one is created, need to persist that token to the old device
        old_device = FitbitAccount.objects.get(identifier=device.identifier)
        old_device.token_type = device.token_type
        old_device.access_token = device.access_token
        old_device.refresh_token = device.refresh_token
        old_device.is_active = True
        old_device.save()

        #device.delete()
        log.info('Reauthorized fitbit account %s with fresh authentication tokens.', device.identifier)

        if old_device.subject.pk != device.subject.pk:
            log.warning('Attempt to register fitbit account %s to subject %s when it\'s already paired to %s.',
                        old_device.identifier,
                        device.subject.email,
                        old_device.subject.email)

            return render(request, 'fitbit_auth_failed.html')
        else:
            return render(request, 'fitbit_reauth_complete.html')

    except FitbitAccount.DoesNotExist:
        device.timezone = profile['timezone']
        device_tz = pytz_tz(device.timezone)
        device.save()

        for participant_study in participant_studies:
            LastUpdatedForStudy.objects.create(
                device=device,
                study=participant_study.study,
                last_updated=participant_study.study.start_date
                )

        fitbit_start_subscription(device)

        return render(request, 'fitbit_auth_complete.html', {'subject': subject})


@csrf_exempt
def fitbit_receive_notification(request):
    if 'verify' in request.GET:
        if '0e858a00cd034d0c80470b36102c16ec01cbe619410b0e5527c26a15d200c6b9' == request.GET['verify']:
            return HttpResponse(status=204)
        else:
            return HttpResponse(status=404)

    try:
        # two steps to validating notification before processing
        # first, confirm forward/reverse DNS lookup
        ip = get_real_ip(request)
        name = socket.gethostbyaddr(ip)[0]
        reversed_addr = socket.gethostbyname(name)
        dns_valid = reversed_addr == ip and name.endswith('fitbit.com')

        signature_valid = False
        reason = None

        if dns_valid:
            # second, verify the HMAC-SHA1 signature in the notification headers
            signature = request.META['HTTP_X_FITBIT_SIGNATURE'].encode('utf8')
            digester = hmac.new(('36408b69aa9977c4f991b4255ac16af7' + '&').encode('utf8'), request.body,
                                digestmod='sha1')
            expected_signature = base64.b64encode(digester.digest())
            signature_valid = hmac.compare_digest(signature, expected_signature)

            if signature_valid:
                notifications = json.loads(request.body.decode('utf8'))

                devices_notified = set()
                #for notification in notifications:
                    #owner_id = notification['ownerId']
                    #fitbit_update_activity_data.delay(owner_id)
                    #devices_notified.add(owner_id)

                log.info(
                    'Received validated notification for devices %s from IP %s, sending async jobs to update data.',
                    devices_notified, ip)
            else:
                reason = 'failed to validate fitbit signature in header'
        else:
            reason = 'failed to validate forward/reverse DNS'

        if not dns_valid or not signature_valid:
            log.warning('Recieved potentially forged notification (%s)! Request META:\n%s\nRequest body:%s',
                        reason, pprint.pformat(request.META, indent=2), request.body)

    except Exception as e:
        log.error('Unable to parse or handle notification received! %s', e)

    return HttpResponse(status=204)

def participants(request):

    #add a new participant
    try:
        importForm = CreateParticipantForm(request.POST)

        if importForm.is_valid():
            saved = importForm.save()
            log.info('Created new participant: %s', saved.pk)
        elif importForm.data['email'] != '':
            try:
                subject = Participant.objects.get(email=importForm.data['email'])

                subject_dict = model_to_dict(subject)

                print(subject_dict)
                print(importForm.data)
                tmp_num = ''
                for key in importForm.data:

                    print(key)

                    if key == 'csrfmiddlewaretoken' or key == 'active':
                        continue

                    if importForm.data[key] != subject_dict[key]:
                        raise ValueError

                importForm = CreateParticipantForm()

            except Participant.DoesNotExist:
                log.warning('participant dont exist, boss')

            except ValueError:
                log.warning('Cannot create a new participant with the same email')
        else:
            importForm = CreateParticipantForm(initial={'active': True})
    except:
        importForm = CreateParticipantForm(initial={'active': True})

    #creating csv file and returning it to user for download
    try:
        file_name = request.POST['file_name']

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="%s"' % file_name

        writer = csv.writer(response)
        writer.writerow(['first_name', 'last_name', 'sex', 'gender', 'email', 'phone'])
        for participant in participants:
            writer.writerow([participant.first_name,
                            participant.last_name,
                            participant.sex,
                            participant.gender,
                            participant.email,
                            participant.phone])

        return response
    except KeyError:
        file_name = "participants_" + user_id + ".csv"
        downloadForm = ParticipantDownloadForm(initial={'file_name': file_name})

    args = {
        'participants_data': participants_data,
        'importForm': importForm,
        'user_id': user_id,
        'downloadForm': downloadForm,
        'user_is_admin': user_is_admin,
        'username': request.user.username,
        }

    return render(request,'participants.html', args)

def study(request, study_id):
    user_is_admin = request.user.is_staff
    has_study = True
    study = Study.objects.get(pk=study_id)

    try:
        downloadDataForm = StudyDownloadDataForm(request.POST)
        if downloadDataForm.is_valid():
            user = request.user

            ResearcherHasStudy.objects.get(study=study, researcher=user)

            if datetime.date.today() < study.start_date:
                return HttpResponse('Study hasn\'t started yet!')  # TODO return proper template

            #get subjects in study
            participants = StudyHasParticipant.objects.filter(study=study).values_list('participant')

            if participants.count() == 0:
                return HttpResponse('No subjects enrolled in study yet!')  # TODO return proper template error

            num_records = 0

            for participant in participants:

                try:
                    fitbit = FitbitAccount.objects.get(subject=participant)
                    num_records += FitbitMinuteRecord.objects.filter(device=fitbit).count()
                except FitbitAccount.DoesNotExist:
                    continue

            if num_records == 0:
                return HttpResponse('No fitbit data recorded yet!')  # TODO return proper template error
            start_date = downloadDataForm.data['start_date']
            end_date = downloadDataForm.data['end_date']
            create_zip_export_bytes(study.pk, user.pk, start_date, end_date)
        else:
            downloadDataForm = StudyDownloadDataForm(initial={
                'download': True,
                'start_date': study.start_date,
                'end_date': study.end_date
                })
    except:
        downloadDataForm = StudyDownloadDataForm(initial={
                'download': True,
                'start_date': study.start_date,
                'end_date': study.end_date
                })

    try:
        study = ResearcherHasStudy.objects.get(study=study_id, researcher=request.user).study
    except:
        has_study = False
        return render(request, 'study.html', {"has_study": has_study})

    if not study.active:
        return render(request, 'study_does_not_exist.html')

    #trying to add participant to study
    try:
        form = AddParticipantToStudyForm(request.POST, researcher=request.user)
        if form.is_valid():
            saved = form.save()
            log.info('Added participant %d to study %s', saved.participant.pk, saved.study.pk)
            participant_link = fitbit_build_auth_url(saved.participant)
            emailParticipant([saved.participant.email], study.pk, participant_link)
            try:
                device = FitbitAccount.objects.get(subject=saved.participant)
                log.info('Participant %d updated for study %s @ %s', saved.participant.pk, saved.study.pk, saved.study.start_date)
            except:
                log.info('Participant %d does not have a Fitbit registered with WearWare', saved.participant.pk)
        else:
            form = AddParticipantToStudyForm(initial={'study': study.pk, 'active': True}, researcher=request.user)
    except:
        form = AddParticipantToStudyForm(initial={'study': study.pk, 'active': True}, researcher=request.user)

    #trying to remove researcher from study
    try:
        removeResearcherForm = RemoveResearcherFromStudy(request.POST, study=study, user=request.user)
        if form.is_valid():
            ResearcherHasStudy.objects.get(researcher=form.data['reseracher'], study=form.data['study']).delete()
            log.info('Successfully removed researcher %s from study %s', form.data['researcher'].pk, form.data['study'].pk)
        else:
            removeResearcherForm = RemoveResearcherFromStudy(study=study, user=request.user)
    except:
        removeResearcherForm = RemoveResearcherFromStudy(study=study, user=request.user)

    # try to export participants in study to a csv file
    try:
        file_name = request.POST['file_name']

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="%s"' % file_name

        writer = csv.writer(response)
        writer.writerow(['first_name', 'last_name', 'sex', 'gender', 'email', 'data_collection_start_date'])

        for study_participant in study_participants:
            participant = study_participant.participant
            writer.writerow([participant.first_name,
                            participant.last_name,
                            participant.sex,
                            participant.gender,
                            participant.email,
                            study_participant.data_collection_start_date])

        return response
    except:
        file_name = "participants_" + request.user.username + ".csv"
        downloadForm = ParticipantDownloadForm(initial={'file_name': file_name})

    args = {
        'study': study,
        'user_is_admin': user_is_admin,
        'username': request.user.username,
        'form': form,
        'participants_data': participants_data,
        "has_study": has_study,
        'rm_researcher_form': RemoveResearcherForm,
        'study_download_form': StudyDownloadDataForm
        }

    return render(request,'study.html', args)