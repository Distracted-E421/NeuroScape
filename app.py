
from flask import Flask, render_template, request, redirect, url_for
from db import db, Task, init_db
from google_api import init_google_client, get_user_token, add_event

app = Flask(__name__,)
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