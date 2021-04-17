from sqlalchemy import create_engine
from requests_oauthlib import OAuth2Session
from django.core.mail import send_mail
def new_participant_signup(participant_email,participant_study):
	authorization_url = fitbit_build_auth_url()
	send_mail(
		'You have been invited to join an NAU informatics study: '+participant_study,
		'Please click the following link to allow wearableinformatics to access your fitbit data:'+authorization_url,
		'wearableinformaticstest2@gmail.com',
		[participant_email],
		fail_silently=False,
	)


#Construct an authentication URL for a given subject.
#scope can be changed to change which data 
#wearware will have access to
def fitbit_build_auth_url():
    params = {
        'client_id': client_id,
        'response_type': 'code',
        'scope': 'activity heartrate location sleep profile',
    }
    url_parts = list(urlsplit(fitbit_auth_url))
    url_parts[3] = urlencode(params)
    auth_url = urlunsplit(url_parts)
    return auth_url