from google.oauth2.credentials import Credentials
from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow, InstalledAppFlow
from google.auth.transport.requests import Request
import json
import os

# Define the scopes
SCOPES = ['https://www.googleapis.com/auth/calendar']

# Initialize the Google API client
flow = InstalledAppFlow.from_client_secrets_file(
    'client_secret.json', SCOPES)

def init_google_client():
    if not os.path.exists('token.json'):
        flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(json.dumps(flow.credentials.to_json()))
    else:
        with open('token.json', 'r') as token:
            creds_data = json.loads(token.read())
        flow.credentials = google.oauth2.credentials.Credentials.from_authorized_user_info(creds_data)

    return flow


def get_user_token():
    # Code to get user token goes here
    pass

def add_event():
    # Code to add event goes here
    pass