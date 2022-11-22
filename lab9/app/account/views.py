
from flask import render_template, request, redirect, flash, url_for, abort
from flask_login import login_user, current_user, logout_user, login_required
from urllib.parse import urlparse, urljoin
import platform
from datetime import datetime

from .forms import RegistrationForm, LoginForm
from app.models import User
from .. import db, bcrypt

from . import account_bp


navs = [
    {
        "name" : "Home",
        "url" : "home"
    },
    {
        "name" : "About",
        "url" : "about"
    },
    {
        "name" : "Contact",
        "url" : "contact"
    },
    {
        "name": "Projects",
        "url": "projects"
    },
    {
        "name": "Persons info",
        "url": "person_info"
    },
    {
        "name": "Users",
        "url": "users"
    },
    {
        "name": "Log in",
        "url": "login"
    },
    {
        "name": "Register",
        "url": "register"
    },

]


def footer_l_get():
    return [platform.platform(),
              request.headers.get('User-Agent'),
              datetime.now()
              ]


@account_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:  # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        return redirect(url_for("home"))
    form = RegistrationForm()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = bcrypt.generate_password_hash(form.password.data)

        user = User(username=username, email=email, hashed_password=password)
        db.session.add(user)
        db.session.commit()

        flash(f'Account created for {form.username.data} !', category='success')
        return redirect(url_for('login'))
    return render_template('register.html',
                           form=form,
                           navs=navs,
                           footer_l=footer_l_get()
                           )


def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
           ref_url.netloc == test_url.netloc


@account_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        user = User.query.filter_by(email=email).first()

        if user and user.verify_password(form.password.data):
            login_user(user, remember=form.remember.data)
            flash(f"You have been logged in", category='success')
            next = request.args.get('next')

            if not is_safe_url(next):
                return abort(400)
            # print(user.verify_password(form.password.data))
            return redirect(next or url_for('home.home'))



        else:
            flash(f"Incorrect input data", category='danger')
    return render_template('login.html',
                           form=form,
                           navs=navs,
                           footer_l=footer_l_get())


@account_bp.route('/logout')
def logout():
    logout_user()
    flash(f"You have been logged out", category='success')
    return redirect(url_for("home.home"))


@account_bp.route('/users')
def users():
    if current_user.is_authenticated:
        log_in = User.query.filter_by(id=current_user.get_id()).first()
    else:
        log_in = False
    all_users = User.query.all()
    return render_template('users.html',
                           log_in=log_in,
                           all_users=all_users,
                           navs=navs,
                           footer_l=footer_l_get()
                           )


@account_bp.route('/account')
@login_required
def account():
    if current_user.is_authenticated:
        log_in = User.query.filter_by(id=current_user.get_id()).first()
    else:
        log_in = False
    return render_template('account.html',
                           log_in=log_in,
                           navs=navs,
                           footer_l=footer_l_get()
                           )

