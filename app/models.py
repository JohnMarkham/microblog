from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime
from app import db

class User(db.Model):
    '''User Class'''

    '''These are Class variables defined here because that's how SQLAlchemy knows the table structure'''
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(120), index = True, unique = True)
    username = db.Column(db.String(64), index = True, unique = True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Post', backref='author', lazy = 'dynamic')



    def __init__(self, username = None, email = None, posts = None):
        self.username = username
        self.email = email
        self.posts = posts

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    body = db.Column(db.String(256))
    timestamp = db.Column(db.DateTime, index = True, default = datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post {}>'.format(self.body)