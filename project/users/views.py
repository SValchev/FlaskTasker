from functools import wraps
from flask import session, flash, redirect, url_for, request, render_template, Blueprint
from sqlalchemy.exc import IntegrityError

from project.models import User
from project import db, bcrypt
from .forms import LoginForm, RegistrationForm

###########
##configs##
###########

users_blueprint = Blueprint('users', __name__)


####################
##helper functions##
####################

def login_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return test(*args, **kwargs)
        else:
            flash("You need to logg in first!")
            return redirect(url_for('users.login'))

    return wrap


#################
##raute handle##
#################

@users_blueprint.route('/logout/')
@login_required
def log_out():
    session.pop('logged_in', None)
    session.pop('current_user', None)
    session.pop("user_name", None)
    session.pop("role", None)

    flash('Goodbye!')
    return redirect(url_for('users.login'))


@users_blueprint.route('/', methods=['GET', 'POST'])
def login():
    error = None
    form = LoginForm(request.form)

    if 'logged_in' in session:
        flash("You are allready loged in!")
        return redirect(url_for("tasks.tasks"))

    if request.method == 'POST':
        if form.validate_on_submit():
            user = User.query.filter_by(username=request.form['username']).first()
            if user is not None and bcrypt.check_password_hash(user.password, request.form["password"]):
                session['logged_in'] = True
                session['current_user'] = user.user_id
                session["user_name"] = user.username
                session["role"] = user.role
                flash('Welcome!')
                return redirect(url_for('tasks.tasks'))
            else:
                error = "Invalid user or password!"
    return render_template('login.html', form=form, error=error)


@users_blueprint.route('/register/', methods=['GET', 'POST'])
def register():
    error = None
    form = RegistrationForm(request.form)

    if request.method == 'POST':
        if form.validate_on_submit():
            new_user = User(
                username=form.name.data,
                email=form.email.data,
                password=bcrypt.generate_password_hash(form.password.data)
            )

            try:
                db.session.add(new_user)
                db.session.commit()
                flash('Thanks for registrating!')

                return redirect(url_for('users.login'))
            except IntegrityError as e:
                error = "User with the same name or email adress already exists!"
                return render_template('register.html', form=form, error=error)

    return render_template('register.html', form=form, error=error)
