import sqlite3
from flask import current_app, g
from flask_sqlalchemy import SQLAlchemy

# Initialize SQLAlchemy

db = SQLAlchemy()

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    complete = db.Column(db.Boolean, default=False)
    priority = db.Column(db.Integer, default=5)
    priority_title = db.Column(db.String(100))
    priority_color = db.Column(db.String(100))
    tags = db.Column(db.String(100))
    description = db.Column(db.String(1000))
    image = db.Column(db.String(100))
    google_token = db.Column(db.String(1000))

def init_db(app):
    db.init_app(app)
    with app.app_context():
        db.create_all()

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row
    return g.db

def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()