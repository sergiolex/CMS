from flask import (
    Blueprint,
    request,
    render_template,
    flash,
    g,
    session,
    redirect,
    url_for
)
from werkzeug import check_password_hash, generate_password_hash

from app import db
from app.authentication.constants import ReadRole, CommentRole, WriteRole
from app.authentication.forms import LoginForm, SignupForm
from app.authentication.models import User

mod_auth = Blueprint('auth', __name__, url_prefix='/auth')

@mod_auth.route('/signout')
def signout():
    session.clear()
    return redirect(url_for('auth.signin'))

@mod_auth.route('/profile')
def profile():

    if 'token' not in session:
        return redirect(url_for('auth.signin'))

    user = User.verify_token(session['token'])
    if user is None:
        return redirect(url_for('auth.signin'))
    else:
        return render_template('authentication/profile.html')

@mod_auth.route('/signup/', methods=['GET', 'POST'])
def signup():

    form = SignupForm()

    if ('token' in session) and (User.verify_token(session['token'])):
        return redirect(url_for('auth.profile'))
    
    if request.method == 'POST':
        if form.validate() == False:
            return render_template("authentication/signup.html", form=form)
        else:
            new_user = User(form.username.data, form.email.data,\
             form.password.data,ReadRole+CommentRole+WriteRole,1)
            db.session.add(new_user)
            db.session.commit()
            session['email'] = new_user.email
        return redirect(url_for('auth.profile'))
        
    elif request.method == 'GET':
        return render_template("authentication/signup.html", form=form)

@mod_auth.route('/signin/', methods=['GET', 'POST'])
def signin():

    if 'token' in session:
        user = User.verify_token(session['token'])
        if user:
            return redirect(url_for('auth.profile'))
    form = LoginForm(request.form)
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if(user is None):
            flash('invalid email', 'error-message')
        elif (user.check_password(form.password.data) == True):
            session['user_id'] = user.id
            session['token'] = user.generate_token()
            session['email'] = user.email
            return redirect(url_for('auth.profile'))
        else:
            flash('invalid password', 'error-message')


    return render_template("authentication/signin.html", form=form)
