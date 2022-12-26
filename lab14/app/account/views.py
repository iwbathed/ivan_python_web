
from flask import render_template, request, redirect, flash, url_for, abort, current_app
from flask_login import login_user, current_user, logout_user, login_required, current_user
from urllib.parse import urlparse, urljoin
import platform
from datetime import datetime

import os
import secrets
from PIL import Image, ImageOps

from .forms import RegistrationForm, LoginForm, UpdateAccountForm, ChangePasswordForm
from app.models import User, navs, footer_l_get
from .. import db, bcrypt

from . import account_bp


def footer_l_get():
    return [platform.platform(),
              request.headers.get('User-Agent'),
              datetime.now()
              ]


@account_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:  # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        return redirect(url_for("home.home"))
    form = RegistrationForm()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')

        #password = form.password.data
        
        user = User(username=username, email=email, hashed_password=password)
        db.session.add(user)
        db.session.commit()

        flash(f'Account created for {form.username.data} !', category='success')
        return redirect(url_for('account.login'))
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
        return redirect(url_for("account.account"))
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


@account_bp.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    if current_user.is_authenticated:
        log_in = User.query.filter_by(id=current_user.get_id()).first()
    else:
        log_in = False
    form = UpdateAccountForm()
    if request.method == "GET":
        pass_form = ChangePasswordForm()

        image_file = url_for('static', filename="imgs/user_profile_img/" + current_user.image)
        return render_template('account.html',
                               form=form,
                               log_in=log_in,
                               navs=navs,
                               footer_l=footer_l_get(),
                               image_file=image_file,
                               pass_form=pass_form
                           )

    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        image = form.image.data
        about_me = form.about_me.data

        if image:
            current_user.image = save_picture(image)

        current_user.username = username
        current_user.email = email
        current_user.about_me = about_me

        db.session.add(current_user)
        db.session.commit()

        flash(f"Account info successfully updated", category='success')
        return redirect(url_for("account.account"))

    return redirect(url_for("account.account"))
    # return render_template('account.html',
    #                        log_in=log_in,
    #                        navs=navs,
    #                        footer_l=footer_l_get()
    #                        )


def save_picture(from_picture):
    random_hex = secrets.token_hex(8)
    f_name, f_ext = os.path.splitext(from_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/imgs/user_profile_img', picture_fn)
    from_picture.save(picture_path)

    output_size = (125, 125)
    image = Image.open(from_picture)
    thumb = ImageOps.fit(image, output_size, Image.ANTIALIAS)
    thumb.save(picture_path)

    return picture_fn


@account_bp.route('/change_password', methods=['POST'])
@login_required
def change_pwd():
    pass_form = ChangePasswordForm()
    if pass_form.validate_on_submit():
        password = bcrypt.generate_password_hash(pass_form.new_password.data).decode('utf-8')
        
        #password = pass_form.new_password.data
        current_user.hashed_password = password
        db.session.add(current_user)
        db.session.commit()

        flash(f"Account info successfully updated", category='success')
        return redirect(url_for("account.account"))
    flash(f"Not correct data passed", category='warning')
    return redirect(url_for("account.account"))

