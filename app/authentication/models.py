from app import db
from werkzeug import generate_password_hash, check_password_hash

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

    def check_password(self, password):
        return check_password_hash(self.pwdhash, password)
