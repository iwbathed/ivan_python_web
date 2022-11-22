

import platform
from datetime import datetime



from . import home_bp
from .. import db, bcrypt

from flask import render_template, request, redirect

from app.models import User
from flask_login import login_user, current_user, logout_user, login_required




# home_bp.config['SECRET_KEY'] = 'SSSqwed453rvsdf4df'



contact_l = {


    "mails" : [
        "my_super_mail@email.com",
        "my_second_mail@email.com",
        "main_mail@email.com",
    ],
    "phones" : [
        "0989999999",
        "0688888888",
        "55-68-35"
    ],

}


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


@home_bp.route('/index')
@home_bp.route('/')
def start():
    return redirect("/home")


@home_bp.route('/home')
def home():
    if current_user.is_authenticated:
        log_in = User.query.filter_by(id=current_user.get_id()).first()
    else:
        log_in = False
    # print("log_in", log_in)
    return render_template('index.html',
                           log_in=log_in,
                           navs=navs,
                           footer_l=footer_l_get())


@home_bp.route('/about')
def about():
    if current_user.is_authenticated:
        log_in = User.query.filter_by(id=current_user.get_id()).first()
    else:
        log_in = False
    return render_template('about.html',
                           log_in=log_in,
                           navs=navs,
                           footer_l=footer_l_get())


@home_bp.route('/projects')
def projects():
    if current_user.is_authenticated:
        log_in = User.query.filter_by(id=current_user.get_id()).first()
    else:
        log_in = False
    return render_template('projects.html',
                           log_in=log_in,
                           navs=navs,
                           footer_l=footer_l_get())

