from flask import request
from app import db
from werkzeug import generate_password_hash, check_password_hash
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)




class User(db.Model):

    __tablename__ = 'auth_user'
    
    id       = db.Column('id', db.Integer, primary_key=True, \
                autoincrement='ignore_fk')
    username = db.Column(db.String(128),  nullable=False, unique=True)
    email    = db.Column(db.String(128),  nullable=False, unique=True)
    password = db.Column(db.String(128),  nullable=False)
    role     = db.Column(db.SmallInteger, nullable=False)
    status   = db.Column(db.SmallInteger, nullable=False)

    def __init__(self, username, email, password,role,status):

        self.username = username.title()
        self.email    = email.lower()
        self.password = generate_password_hash(password)
        self.role     = role
        self.status   = status

    def __repr__(self):
        return '<User %r>' % (self.username)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def generate_token(self, expiration = 600):
        s = Serializer('key_word')
        return s.dumps({'id': self.id, 'username':self.username, \
        'email':self.email,'ip_address': request.remote_addr})

    @staticmethod
    def verify_token(token):
        s = Serializer('key_word')
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None # valid token, but expired
        except BadSignature:
            return None # invalid token
        user = User.query.get(data['id'])
        return user
