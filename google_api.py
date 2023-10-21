from google.oauth2.credentials import Credentials
from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow, InstalledAppFlow
from google.auth.transport.requests import Request
from flask import current_app, redirect, url_for, session
from app import db, User
import json
import os


# Define the scopes
SCOPES = ['https://www.googleapis.com/auth/calendar']

# Initialize the Google API client
flow = InstalledAppFlow.from_client_secrets_file(
    'client_secret.json', SCOPES)

def init_google_client():
    client_id = current_app.config.get('GOOGLE_CLIENT_ID')
    client_secret = current_app.config.get('GOOGLE_CLIENT_SECRET')
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
        # TODO: Implement OAuth2 flow to get user token and store it in the database
        # This function will be called during account creation and login.
        # It will redirect the user to a Google sign-in page (HTML template: google_signin.html)
        # and then handle the OAuth2 callback to get and store the user token.
    pass
def start_oauth_flow():
# Start the OAuth2 flow
    authorization_url, state = flow.authorization_url(
        'https://accounts.google.com/o/oauth2/auth',
        access_type='offline',
        prompt='consent'
    )
    session['state'] = state
    return redirect(authorization_url)

def handle_oauth_callback():
    if 'state' not in session or 'state' not in request.args:
        return 'Invalid state parameter', 400
    if session['state'] != request.args['state']:
        return 'Invalid state parameter', 400

    flow.fetch_token(authorization_response=request.url)

            # Store the user token in the database
    user_info = id_token.verify_oauth2_token(
        flow.credentials.id_token, Request())
    user = User.query.filter_by(email=user_info['email']).first()

    if not user:
        user = User(email=user_info['email'])
        db.session.add(user)
        user.google_token = json.dumps(flow.credentials.to_json())
        db.session.commit()

        return redirect(url_for('index'))
        # TODO: Implement OAuth2 flow to get user token and store it in the database
        # This function will be called during account creation and login.
        # It will redirect the user to a Google sign-in page (HTML template: google_signin.html)
        # and then handle the OAuth2 callback to get and store the user token.

def start_oauth_flow():
    authorization_url, state = flow.authorization_url(
        'https://accounts.google.com/o/oauth2/auth',
        access_type='offline',
        prompt='consent'
    )
    session['state'] = state
    return redirect(authorization_url)

def add_event():
            pass