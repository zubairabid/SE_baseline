from datetime import datetime
from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from hashlib import md5

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

asgn_user = db.Table('association',
        db.Column('user_id', db.Integer, db.ForeignKey('assignment.id'), primary_key=True),
        db.Column('asgn_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
)

class Submissions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    aid = db.Column(db.Integer, index=True)
    uid = db.Column(db.Integer, index=True)
    imglink = db.Column(db.String(140), unique=True)
    submitted = db.Column(db.Boolean)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    name = db.Column(db.String(120), index=False, unique=False)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    teacher = db.Column(db.Boolean)

    #posts = db.relationship('Post', backref='author', lazy='dynamic')
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def set_teacher(self, value):
        self.teacher = value

    def get_teacher(self):
        return self.teacher

class Assignment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    setter_username = db.Column(db.String(64), index=False, unique=False)
    q1 = db.Column(db.String(512), index=False, unique=False)
    q2 = db.Column(db.String(512), index=False, unique=False)
    q3 = db.Column(db.String(512), index=False, unique=False)
    a1 = db.Column(db.String(16384), index=False, unique=False)
    a2 = db.Column(db.String(16384), index=False, unique=False)
    a3 = db.Column(db.String(16384), index=False, unique=False)
    users = db.relationship('User', secondary=asgn_user, lazy=True, backref=db.backref('asgns', lazy=True))

    def get_id(self):
        return self.id
