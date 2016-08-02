from app import db
from werkzeug import generate_password_hash, check_password_hash
import datetime

from webhelpers.date import time_ago_in_words
from webhelpers.text import urlify
from flask import jsonify
from itsdangerous import (TimedJSONWebSignatureSerializer
                                  as Serializer, BadSignature, SignatureExpired)

class User(db.Model):

    __tablename__ = 'auth_user'
    
    id       = db.Column('id', db.Integer, primary_key=True, autoincrement='ignore_fk')
    username = db.Column(db.String(128),  nullable=False)
    email    = db.Column(db.String(128),  nullable=False,
                      unique=True)
    password = db.Column(db.String(128),  nullable=False)
    role     = db.Column(db.SmallInteger, nullable=True)
    status   = db.Column(db.SmallInteger, nullable=True)

    def __init__(self, username, email, password):

        self.username = username.title()
        self.email    = email.lower()
        self.password = generate_password_hash(password)

    def __repr__(self):
        return '<User %r>' % (self.name)

    def set_password(self, password):
        self.pwdhash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.pwdhash, password)

    def generate_auth_token(self, expiration=600):
        s = Serializer(app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'id': self.id})

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None         #Expired token
        except BadSignature:
            return None         #Invalid token
        user =  User.query.get(data['id'])
        return user

class Article(db.Model):
    __tablename__ = 'articles'
    id        = db.Column('id', db.Integer, primary_key=True, autoincrement='ignore_fk')
    title     = db.Column(db.String(100))
    body      = db.Column(db.Text)
    created   = db.Column(db.DateTime, default=datetime.datetime.now)
    user_name = db.Column(db.String(100), db.ForeignKey(User.username, onupdate="CASCADE",
                        ondelete="CASCADE"))
    user      = db.relationship(User)

    @classmethod
    def all(cls):
        return Article.query_order_by(desc(Article.created)).all()

    @classmethod
    def find_by_id(cls, id):
        return Article.query.filter(Article.id == id).first()

    @classmethod
    def find_by_author(cls, name):
        return Article.query.filter(Article.user_name == name).all()

    @property
    def slug(self):
        return urlify(self.title)

    @property
    def created_in_words(self):
        return time_ago_in_words(self.created)

