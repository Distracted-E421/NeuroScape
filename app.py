
from flask import Flask, render_template, request, redirect, url_for
from db import db, Task, init_db
from google_api import init_google_client, get_user_token, add_event
from authlib.integrations.flask_client import OAuth

app = Flask(__name__,)

# Initialize Google OAuth
from google.oauth2 import WebApplicationClient
import requests

# OAuth 2 client setup
CLIENT_ID = 'YOUR_GOOGLE_CLIENT_ID'
GOOGLE_DISCOVERY_URL = 'https://accounts.google.com/.well-known/openid-configuration'
client = WebApplicationClient(CLIENT_ID)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize db
init_db(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/google-login')
def google_login():
    # Find out what URL to hit for Google login
    google_provider_cfg = requests.get(GOOGLE_DISCOVERY_URL).json()
    authorization_endpoint = google_provider_cfg['authorization_endpoint']

    # Use library to construct the request for Google login
    request_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=request.base_url + '/callback',
        scope=['openid', 'email', 'profile'],
    )
    return redirect(request_uri)


if __name__ == '__main__':
    app.run(debug=True)