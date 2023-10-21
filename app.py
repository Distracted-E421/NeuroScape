
from flask import Flask, render_template, request, redirect, url_for
from db import db, Task, init_db
from google_api import init_google_client, get_user_token, add_event
import requests

app = Flask(__name__,)

# Initialize Google OAuth with FastAPI OAuth2
from fastapi.security import OAuth2AuthorizationCodeBearer

oauth2_scheme = OAuth2AuthorizationCodeBearer(tokenUrl='https://oauth2.googleapis.com/token')
authorizationUrl='https://accounts.google.com/o/oauth2/auth',
tokenUrl='https://accounts.google.com/o/oauth2/token',
clientId='80048219165-jhs4kk14n3iub1mn56vgkicc4si9fvph.apps.googleusercontent.com',
clientSecret='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',
scopes=['openid', 'email', 'profile']



# OAuth 2 client setup
# Load client secrets from your Google Cloud Console
import json

with open('path/to/client_secret.json', 'r') as f:
    GOOGLE_CLIENT_INFO = json.load(f)

CLIENT_ID = GOOGLE_CLIENT_INFO['web']['client_id']
CLIENT_SECRET = GOOGLE_CLIENT_INFO['web']['client_secret']
REDIRECT_URI = GOOGLE_CLIENT_INFO['web']['redirect_uris'][0]
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
    authorization_url = oauth2_scheme.get_authorization_url()
    return redirect(authorization_url)
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


@app.route('/callback')
def callback():
    code = request.args.get('code')
    token = oauth2_scheme.get_token(code)
    user_info = oauth2_scheme.get_user_info(token)
    # TODO: Create user in your db with the information provided by Google
    return 'Logged in as: ' + user_info['email'], 200
def callback():
    # Get authorization code Google sent back to you
    code = request.args.get('code')
    google_provider_cfg = requests.get(GOOGLE_DISCOVERY_URL).json()
    token_endpoint = google_provider_cfg['token_endpoint']

    token_url, headers, body = client.prepare_token_request(
        token_endpoint,
        authorization_response=request.url,
        redirect_url=request.base_url,
        code=code
    )
    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(CLIENT_ID, 'YOUR_GOOGLE_CLIENT_SECRET'),
    )

    client.parse_request_body_response(json.dumps(token_response.json()))

    userinfo_endpoint = google_provider_cfg['userinfo_endpoint']
    uri, headers, body = client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)

    if userinfo_response.json().get('email_verified'):
        unique_id = userinfo_response.json()['sub']
        users_email = userinfo_response.json()['email']
        picture = userinfo_response.json()['picture']
        users_given_name = userinfo_response.json()['given_name']
        users_family_name = userinfo_response.json()['family_name']
    else:
        return 'User email not available or not verified by Google.', 400

        # TODO: Create user in your db with the information provided by Google

        return 'Logged in as: ' + users_email, 200


if __name__ == '__main__':
    app.run(debug=True)