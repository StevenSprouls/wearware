from flask import Flask, request, session, redirect, session, url_for
from requests_oauthlib import OAuth2Session
from flask.json import jsonify
from urllib.parse import urlsplit, urlencode, urlunsplit, urlparse
import os
import sys
import json

client_id = '22C4KD'
client_secret = 'd25cd8564b744d78b92b920e074bb555'
fitbit_auth_url = 'https://www.fitbit.com/oauth2/authorize'
fitbit_auth_token = 'https://api.fitbit.com/oauth2/token'

app = Flask(__name__)
app.secret_key = os.urandom(24)

#index landing page, will be changed upon migration to Amazon EC2
@app.route('/')
def hello():
    fitbit = OAuth2Session(client_id)
    authorization_url = fitbit_build_auth_url()
    return redirect(authorization_url)


#callback url, will be changed upon migration to Amazon EC2
@app.route('/callback', methods=["GET"])
def callback():
    fitbit = OAuth2Session(client_id)
    token = fitbit.fetch_token(fitbit_auth_token, client_secret=client_secret,
                               authorization_response=request.url)
    session['oauth_token'] = token
    return redirect(url_for('.activity'))

#
@app.route('/activity', methods=["GET"])
def activity():
    fitbit = OAuth2Session(client_id, token=session['oauth_token'])
    response = fitbit.get('https://api.fitbit.com/1/user/-/activities/heart/date/today/1d.json').json()
    return json.dumps(response)

#Construct an authentication URL for a given subject.
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


if __name__ == "__main__":
    # This allows us to use a plain HTTP callback
    app.run(debug=True)
