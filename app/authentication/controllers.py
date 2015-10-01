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
from app.authentication.forms import LoginForm, SignupForm
from app.authentication.models import User

mod_auth = Blueprint('auth', __name__, url_prefix='/auth')

@mod_auth.route('/signup/', methods=['GET', 'POST'])
def signup():

    form = SignupForm()
    
    if request.method == 'POST':
        if form.validate() == False:
            return render_template("authentication/signup.html", form=form)
        else:
            new_user = User(form.username.data, form.email.data, form.password.data)
            db.session.add(new_user)
            db.session.commit()

            session['email'] = new_user.email
            return "Not found"
        
    elif request.method == 'GET':
        return render_template("authentication/signup.html", form=form)


@mod_auth.route('/signin/', methods=['GET', 'POST'])
def signin():

    form = LoginForm(request.form)
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            session['user_id'] = user.id
            flash('Welcome %s' % user.name)
            return redirect(url_for('auth.home'))

        flash('Wrong email or password', 'error-message')

    return render_template("authentication/signin.html", form=form)
