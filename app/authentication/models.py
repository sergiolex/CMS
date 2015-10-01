from app import db
from werkzeug import generate_password_hash, check_password_hash


class Base(db.Model):

    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime,
                              default=db.func.current_timestamp(),
                              onupdate=db.func.current_timestamp())


class User(Base):

    __tablename__ = 'auth_user'

    username = db.Column(db.String(128),  nullable=False)
    email = db.Column(db.String(128),  nullable=False,
                      unique=True)
    password = db.Column(db.String(192),  nullable=False)
    role = db.Column(db.SmallInteger, nullable=False)
    status = db.Column(db.SmallInteger, nullable=False)

    def __init__(self, username, email, password):

        self.username = username
        self.email = email
        self.password = password

    def set_password(self, password):
        self.pwdhash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.pwdhash, password)

    def __repr__(self):
        return '<User %r>' % (self.name)
