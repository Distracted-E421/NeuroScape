
from flask import Flask, render_template, request, redirect, url_for
from db import db, Task, init_db
from google_api import init_google_client, get_user_token, add_event

app = Flask(__name__,)
from authlib.integrations.flask_client import OAuth

# Initialize OAuth
oauth = OAuth(app)
google = oauth.remote_app(
    'google',
    client_id='YOUR_GOOGLE_CLIENT_ID',
    client_secret='YOUR_GOOGLE_CLIENT_SECRET',
    request_token_params={
        'scope': 'email',
    },
    base_url='https://www.googleapis.com/oauth2/v1/',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://accounts.google.com/o/oauth2/token',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize db
init_db(app)

@app.route('/')
def index():
    return render_template('index.html')

# Add more routes here as needed

if __name__ == '__main__':
    app.run(debug=True)