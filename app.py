# Importing required libraries and modules
from flask import Flask, render_template, request, redirect, url_for
from oauthlib.oauth2 import WebApplicationClient
from flask_migrate import Migrate
from db import db, Task, init_db
from google_api import get_user_token, add_event
import requests
from fastapi.security import OAuth2AuthorizationCodeBearer
import json

# Initialize Flask app and database migration
app = Flask(__name__,)
migrate = Migrate(app, db)

# Initialize Google OAuth with FastAPI OAuth2

with open('client_secret.json', 'r') as f:
    GOOGLE_CLIENT_INFO = json.load(f)

CLIENT_ID = GOOGLE_CLIENT_INFO.get('web', {}).get('client_id', None)
CLIENT_SECRET = GOOGLE_CLIENT_INFO.get('web', {}).get('client_secret', None)
REDIRECT_URI = GOOGLE_CLIENT_INFO.get('web', {}).get('redirect_uris', [None])[0]
GOOGLE_DISCOVERY_URL = 'https://accounts.google.com/.well-known/openid-configuration'

client = WebApplicationClient(CLIENT_ID)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize Google OAuth settings
oauth2_scheme = OAuth2AuthorizationCodeBearer(tokenUrl='https://oauth2.googleapis.com/token', authorizationUrl='https://accounts.google.com/o/oauth2/auth')
authorizationUrl='https://accounts.google.com/o/oauth2/auth',
tokenUrl='https://accounts.google.com/o/oauth2/token',
clientId='80048219165-jhs4kk14n3iub1mn56vgkicc4si9fvph.apps.googleusercontent.com',
clientSecret='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',
scopes=['openid', 'email', 'profile']
# Initialize db
init_db(app)


# TODO: Add logic for Google OAuth callback
def callback():
    # Get authorization code
    code = request.args.get('code')

    # Fetch user token
    token_response = client.prepare_request_uri(
        tokenUrl,
        redirect_uri=REDIRECT_URI,
        scope=['openid', 'email', 'profile'],
        state='random_state_string'
    )
    token_response = get_user_token(code)

    # Extract user info from token
    user_info = requests.get('https://www.googleapis.com/oauth2/v3/userinfo', headers={'Authorization': f'Bearer {access_token}'}).json()
    access_token = token_response['access_token']
    user_info = requests.get('https://www.googleapis.com/oauth2/v3/userinfo', headers={'Authorization': f'Bearer {access_token}'}).json()

    # TODO: Store user info in database

    return 'Logged in as: ' + user_info['email'], 200


@app.route('/')
def home():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)