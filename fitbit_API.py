import fitbit
import gather_keys_oauth2 as Oauth2
import datetime
import random
import sys
sys.path.append("./wearwareAPI/wearware/WearWareRESTAPI")
from models.py import FitbitAccount


#Secret application information
client_id = '22C4KD'
client_secret = 'd25cd8564b744d78b92b920e074bb555'

#configures oauth2 server with client_id and client_secret
server=Oauth2.OAuth2Server(client_id,client_secret)
#uses the server configured to authorize (web page with access request should pop up here)
server.browser_authorize()
#retrieve access token and refresh token
ACCESS_TOKEN=str(server.fitbit.client.session.token['access_token'])
REFRESH_TOKEN=str(server.fitbit.client.session.token['refresh_token'])

#variable with the authorization from Oauth2 and the tokens retrieved
auth2_client=fitbit.Fitbit(client_id,client_secret,oauth2=True,
                           access_token=ACCESS_TOKEN,refresh_token=REFRESH_TOKEN)

#test date for getting 1 day of data from 02/23/2021
#oneDate = datetime(year = 2021, month = 2, day = 28)

def create_new_fitbit_account():  
    user_profile = auth2_client.user_profile_get()
    timezone = user_profile['user']['timezone']
    identifier = random.int(1000,1000000)
    subject = identifier
    is_active = True
    token_type = 'auth_token'
    refresh_token = REFRESH_TOKEN
    access_token = ACCESS_TOKEN
    NewFitbitAccount = models.FitbitAccount(
        identifer,
        subject,
        is_active,
        timezone,
        token_type,
        refresh_token,
        access_token
    )
    return NewFitbitAccount

#cannot currently get intraday activity due to inability to use winfree fitbit
#application with permissions
def make_fitbit_request(fitbitaccount):
    client = fitbit.Fitbit(client_id,client_secret,oauth2=True,
                           access_toekn=fitbitaccount.access_token,
                           refresh_token=fitbitaccount.refresh_token)
    return client.activity_stats()


#Fetches intraday data for heartrate using above date at second level detail
##help(auth2_client.activity_stats)
#oneDayData = auth2_client.intraday_time_series('activities/heart',
      #                                         base_date=oneDate, detail_level='1sec')
#print(oneDayData)
#places data retrieved in a dataframe for ease of use
#df = pd.DataFrame(oneDayData['activities-heart-intraday']['dataset'])
#df.head()

#creates file for csv export
#filename = oneDayData['activities-heart'][0]['dateTime'] +'_intradata'
#print("successfully got to here")
# Export file to csv
#df.to_csv(filename + '.csv', index = False)
