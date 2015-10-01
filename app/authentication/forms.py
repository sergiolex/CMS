from flask.ext.wtf import Form # , RecaptchaField
from wtforms import TextField, PasswordField, SubmitField # BooleanField
from wtforms.validators import Required, Email, EqualTo
from models import db, User


class SignupForm(Form):
    username = TextField('Username', 
            [Required(message='Please enter an username.')])
    email    = TextField('Email Address', [Email(),
                Required(message='Please enter your email address.')])
    password = PasswordField('Password', [
                Required(message='Please enter a password.')])
    submit   = SubmitField("Create account")

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)

    def validate(self):
        if not Form.validate(self):
            return False

        user = User.query.filter_by(email = self.email.data.lower()).first()
        if user:
            self.email.errors.append("That email is already taken.")
            return False
        else:
            return True

class LoginForm(Form):
    email    = TextField('Email Address', [Email(),
                Required(message='Forgot your email address?')])
    password = PasswordField('Password', [
                Required(message='Must provide a password.')])
