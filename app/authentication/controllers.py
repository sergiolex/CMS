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
from app.authentication.forms import LoginForm, SignupForm, ArticleCreateForm
from app.authentication.models import User, Article

mod_auth = Blueprint('auth', __name__, url_prefix='/auth')

@mod_auth.route('/profile/<username>')
def profile(username):
    if 'email' not in session:
        return redirect(url_for('auth.signin'))
    user = User.query_filter_by(email=session['email']).first()
    if username == user.username:
        user = User.query_filter_by(email=session['email']).first()
        username = user.username
        return render_template('user/profile.html', username=username)
    return render_template('user/profile.html')

@mod_auth.route('/create', methods=['GET', 'POST'])
def article_create():
    if 'email' not in session:
        return redirect(url_for('sigin'))
    user     = User.query.filter_by(email=session['email']).first()
    username = user.username
    article  = Article()
    form     = ArticleCreateForm()
    form.user_name.data = user.username
    if form.validate_on_submit():
        form.populate_obj(article)
        db.session.add(article)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('user/create.html', form=form, user=user, username=username)

@mod_auth.route('/signup/', methods=['GET', 'POST'])
def signup():

    form = SignupForm()

    if 'email' is session:
        return redirect(url_for('auth.profile'))
    
    if request.method == 'POST':
        if form.validate() == False:
            return render_template("authentication/signup.html", form=form)
        else:
            new_user = User(form.username.data, form.email.data, form.password.data)
            db.session.add(new_user)
            db.session.commit()

            session['email'] = new_user.email
            user = User.query.filter_by(email=session['email']).first()
            username = user.username
            return "SUCCESS"
            #return redirect(url_for('auth.profile'), username=username)
        
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
