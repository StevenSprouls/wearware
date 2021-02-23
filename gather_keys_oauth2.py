import cherrypy
import os
import sys
import threading
import traceback
import webbrowser

from urllib.parse import urlparse
from base64 import b64encode
from fitbit.api import Fitbit
from oauthlib.oauth2.rfc6749.errors import MismatchingStateError, MissingTokenError

#Function configures Oauth2server with localhost as the callback url
#fitbit is configured to the fitbit_API.py file with client_id and client_secret
#timeout is set to 10 seconds if the server does not communicate properly
class OAuth2Server:
    def __init__(self, client_id, client_secret,
                 redirect_uri='https://127.0.0.1:8080/'):
        self.success_html="""
            <h1>Fitbit Authorization Successful</h1>
        """
        self.failure_html="""
            <h1>Fitbit Unsuccessful</h1>
        """

        self.fitbit = Fitbit(
            client_id,
            client_secret,
            redirect_uri=redirect_uri,
            timeout=10,
        )
        self.redirect_uri = redirect_uri

#Function creates the Oauth url, starts a thread with a new browser
#This uses cherrypy, a localhost library with python, REPLACE WHEN CONNECTING TO OUR WEBSERVER
    def browser_authorize(self):
        url, _ = self.fitbit.client.authorize_token_url()

        threading.Timser(1, webbrowser.open, args=(url,)).start()

        urlparameters = urlparse(self.redirect_uri)
        #REPLACE WHEN CONNECTING TO OUR WEBSERVER
        cherrypy.config.update({'server.socket_host': urlparams.hostname,
                                'server.socket_port': urlparams.port})
        #REPLACE WHEN CONNECTING TO OUR WEBSERVER
        cherrypy.quickstart(self)

    #Initiates when browser opens to localhost. fetches access tokens from fitbit
    #shutsdown the cherrypy after 1 second (required by fitbit) REPLACE WHEN CONNECTING TO OUR WEBSERVER
    def index(self, state, code=None):
        if code:
            self.fitbit.client.fetch_access_token(code)
        self._shutdown_cherrypy()

    #defines how to shutdown cherrypy in index function REPLACE WHEN CONNECTING TO OUR WEBSERVER
    def _shutdown_cherrypy(self):
        if cherrypy.engine.state == cherrypy.engine.states.STARTED:
            threading.Timer(1, cherrypy.engine.exit).start()
            
    #Test function if fitbit_API.py is not configured, asks in commandline the neccessary information
    if __name__ == '__main__':
        if not (len(sys.argv) == 3):
            print("Arguments: client_id and client_secret")
            sys.exit(1)

        server = OAuth2Server(*sys.argv[1:])
        server.browser_authorize()

        profile = server.fitbit.user_profile_get()
        print('You are authorized to access data for the user: {}'.format(
            profile['user']['fullName']))

        print('TOKEN\n=====\n')
        for key, value in server.fitbit.client.session.token.items():
            print('{} = {}'.format(key, value))
        
