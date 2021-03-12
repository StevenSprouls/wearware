import os
import sys
import threading
import traceback
import webbrowser
import requests
import json
from urllib.parse import urlsplit, urlencode, urlunsplit, urlparse
from base64 import b64encode
from fitbit.api import Fitbit
from oauthlib.oauth2.rfc6749.errors import MismatchingStateError, MissingTokenError


client_id = '22C4KD'
client_secret = 'd25cd8564b744d78b92b920e074bb555'

fitbit_auth_url = 'https://www.fitbit.com/oauth2/authorize'


class OAuth2Server:
    def __init__(self, client_id, client_secret,
                 redirect_uri='http://127.0.0.1:8080/'):
        """ Initialize the FitbitOauth2Client """
        self.success_html = """
            <h1>You are now authorized to access the Fitbit API!</h1>
            <br/><h3>You can close this window</h3>"""
        self.failure_html = """
            <h1>ERROR: %s</h1><br/><h3>You can close this window</h3>%s"""

        self.fitbit = Fitbit(
            client_id,
            client_secret,
            redirect_uri=redirect_uri,
            timeout=10,
        )

        self.redirect_uri = redirect_uri


    def browser_authorize(self):
        """
        Open a browser to the authorization url and spool up a CherryPy
        server to accept the response
        """
        #code = "c02fd24e34c2aa6c376514f91088f556f0e97229"
        #self.fitbit.client.fetch_access_token(code)
        auth_url = fitbit_build_auth_url()
        #header = fitbit_build_request_headers()
        #print(auth_url)
        r = requests.post(auth_url)
        r1 = requests.get(auth_url)
        print(r1)
        print(json.loads(r1.text))
        #print(auth_url)
        # Same with redirect_uri hostname and port.
        urlparams = urlparse(self.redirect_uri)

    def index(self, state, code=None, error=None):
        """
        Receive a Fitbit response containing a verification code. Use the code
        to fetch the access_token.
        """
        print("DOES THIS GET CALLED")
        error = None
        if code:
            try:
                self.fitbit.client.fetch_access_token(code)
            except MissingTokenError:
                error = self._fmt_failure(
                    'Missing access token parameter.</br>Please check that '
                    'you are using the correct client_secret')
            except MismatchingStateError:
                error = self._fmt_failure('CSRF Warning! Mismatching state')
        else:
            error = self._fmt_failure('Unknown error while authenticating')
        # Use a thread to shutdown cherrypy so we can return HTML first
        return error if error else self.success_html

    
    ##Functions below generate urls for authorization and request headers.
    #taken from bitbucket wearware
def fitbit_build_auth_url():
    #Construct an authentication URL for a given subject.
    params = {
        'client_id': client_id,
        'response_type': 'code',
        'scope': 'activity heartrate location sleep profile',
    }
    url_parts = list(urlsplit(fitbit_auth_url))
    url_parts[3] = urlencode(params)
    auth_url = urlunsplit(url_parts)
    return auth_url

def fitbit_build_request_headers():
    #Construct shared request headers for fitbit requests.

    #authenticate using client_secret and client_id
    fitbit_auth = client_id + ':' + client_secret
    fitbit_auth = fitbit_auth.encode('utf8')
    auth_header = 'Basic ' + b64encode(fitbit_auth).decode('utf8')

    headers = {
        'Authorization': auth_header,
        'Accept-Locale': 'en_US',
        'Accept-Language': 'en_US',
    }
    return headers

    #def request_fitbit_data(subscriber):
        #subscriber will have fitbit data
        #need sorting function as well as a function for posting data to database

"""
    def fitbit_fetch_permanent_token(temp_token):
    #Use a temporary auth token to retrieve a reusable auth token from Fitbit.
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
    return auth_info"""


"""def fitbit_refresh_access_token(device):
    #Refresh an account's access token.
    headers = fitbit_build_request_headers()

    payload = {
        'grant_type': 'refresh_token',
        'refresh_token': device.refresh_token,
    }

    log.info('Requesting fresh auth token for device_id %s.', device.pk)
    r = requests.post(fitbit_token_url, data=payload, headers=headers)

    # if we get this far, the request succeeded and we did not email an admin
    auth_info = json.loads(r.text)

    # FIXME 
    auth_info.pop('scope')
    auth_info.pop('expires_in')
    #sets a devices access tokens and refresh tokens. TAKEN FROM bitbucket wearware
    #device.token_type = auth_info['token_type']
    #device.access_token = auth_info['access_token']
    #device.refresh_token = auth_info['refresh_token']
    #device.is_active = True
    #device.save()

    refresh_sync = SyncRecord(device=device,
                              start_time=timezone.now(),
                              end_time=timezone.now(),
                              sync_type='fitbit-token-refresh',
                              successful=True,
                              message='Succeeded refreshing token for device.')
    refresh_sync.save()

    log.info('Successfully updated authentication info for fitbit %s.', device.identifier)
"""
