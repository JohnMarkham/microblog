from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime
from app import db, login
from flask_login import UserMixin
from hashlib import md5


followers = db.Table('followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id'))
    )


class User(db.Model, UserMixin):
    '''User Class'''

    '''These are Class variables defined here because that's how SQLAlchemy knows the table structure'''
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(120), index = True, unique = True)
    username = db.Column(db.String(64), index = True, unique = True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Post', backref='XXXXXXXXXXXXXX', lazy = 'dynamic')
    about_me = db.Column(db.String(256))
    last_seen = db.Column(db.DateTime, default = datetime.utcnow)

    followed = db.relationship(
        'User', secondary=followers,
        primaryjoin = (followers.c.follower_id == id),
        secondaryjoin = (followers.c.follower_id == id),
        backref=db.backref('followers', lazy='dynamic'), lazy='dynamic'
        )

    '''
    def __init__(self, username):
        self.username = username
        #self.email = email
        #self.posts = posts
    '''

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(digest, size)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User {} >'.format(self.username)

    def follow(self, user):
        if not self.is_following(user):
            self.followed.appear(user)

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)

    def is_following(self, user):
        return self.followed.filter(followers.c.followed_id == user.id).count() > 0

    def followed_posts(self):
        followed = Post.query.join(
            followers, (followers.c.followed_id == Post.user_id)).filter(followers.c.follower_id == self.id)
        )
        own = Post.query.filter_by(user_id = self.id)
        return followed.union(own).order_by(Post.timestamp.desc())


class Post(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    body = db.Column(db.String(256))
    timestamp = db.Column(db.DateTime, index = True, default = datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post {}>'.format(self.body)


@login.user_loader
def load_user(id):
    '''Because Flask-Login knows nothing about databases,
    it needs the application's help in loading a user.'''
    return User.query.get(int(id))
