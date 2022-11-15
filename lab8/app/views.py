
# -*- coding: UTF-8 -*-

import platform
from datetime import datetime

import logging
from flask import Flask, render_template, request, \
    redirect, url_for, flash, session
from app.forms import Form, RegistrationForm, LoginForm
from app import app, db, bcrypt
from app.models import Person, User
from flask_login import login_user, current_user, logout_user, login_required

logging.basicConfig(filename='app.log', filemode='a',
                    format='%(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

app.config['SECRET_KEY'] = 'SSSqwed453rvsdf4df'

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


@app.route('/index')
@app.route('/')
def start():
    return redirect("/home")


@app.route('/home')
def home():
    if current_user.is_authenticated:
        log_in = User.query.filter_by(id=current_user.get_id()).first()
    else:
        log_in = False
    print("log_in", log_in)
    return render_template('index.html',
                           log_in=log_in,
                           navs=navs,
                           footer_l=footer_l_get())


@app.route('/about')
def about():
    if current_user.is_authenticated:
        log_in = User.query.filter_by(id=current_user.get_id()).first()
    else:
        log_in = False
    return render_template('about.html',
                           log_in=log_in,
                           navs=navs,
                           footer_l=footer_l_get())


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if current_user.is_authenticated:
        log_in = User.query.filter_by(id=current_user.get_id()).first()
    else:
        log_in = False
    form = Form()
    if request.method == 'POST':
        if form.validate_on_submit():
            username = form.name.data
            email = form.email.data

            phone = form.phone.data
            subject = form.subject.data
            message = form.message.data

            session['name'] = username
            session['email'] = email

            contact_info = Person(name=username, email=email,
                                  phone=phone, subject=subject,
                                  message=message
                                  )
            db.session.add(contact_info)
            db.session.commit()

            form.name.data = 'Successfully validate '
            flash(f"Data sent successfully : {username} {email} "
                  f"{phone} {subject} {message}",
                  category='success')
            logging.info(f"Data sent successfully : {username} {email} "
                         f"{phone} {subject} {message}")
            return redirect(url_for("contact"))
        flash("Not validate (Post)", category='warning')
        logging.warning("Not validate (Post)")
        return redirect(url_for("contact"))
    return render_template('contact.html', navs=navs,
                           log_in=log_in,
                           contact_l=contact_l,
                           footer_l=footer_l_get(),
                           form=form,
                           session=session)

    flash("Not validate (Post)", category='warning')
    logging.warning("Not validate (Post)")
    return redirect(url_for("contact"))


@app.route('/projects')
def projects():
    if current_user.is_authenticated:
        log_in = User.query.filter_by(id=current_user.get_id()).first()
    else:
        log_in = False
    return render_template('projects.html',
                           log_in=log_in,
                           navs=navs,
                           footer_l=footer_l_get())


@app.route('/person_info', methods=['GET'])
def persons_info():
    if current_user.is_authenticated:
        log_in = User.query.filter_by(id=current_user.get_id()).first()
    else:
        log_in = False
    contact_info_list = Person.query.all()
    return render_template('person.html',
                           log_in=log_in,
                           contact_info_list=contact_info_list,
                           navs=navs,
                           footer_l=footer_l_get()
                           )


@app.route('/person_info/<id>', methods=['GET'])
def person_info(person_id):
    if current_user.is_authenticated:
        log_in = User.query.filter_by(id=current_user.get_id()).first()
    else:
        log_in = False
    contact_info_list = Person.query.filter_by(id=person_id)
    return render_template('person.html',
                           log_in=log_in,
                           contact_info_list=contact_info_list,
                           navs=navs,
                           footer_l=footer_l_get()
                           )


@app.route('/person/delete/<id>')
def delete_person(person_id):
    if current_user.is_authenticated:
        log_in = User.query.filter_by(id=current_user.get_id()).first()
    else:
        log_in = False
    try:
        Person.query.filter_by(id=person_id).delete()
        db.session.commit()
    except Exception:
        db.session.flush()
        db.session.rollback()
    return render_template('on_delete.html',
                           log_in=log_in,
                           id=person_id,
                           navs=navs,
                           footer_l=footer_l_get()
                           )


@app.route('/register', methods=['GET', 'POST'])
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


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:  # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        return redirect(url_for("home"))
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        user = User.query.filter_by(email=email).first()

        if user and user.verify_password(form.password.data):
            login_user(user, remember=form.remember.data)
            flash(f"You have been logged in", category='success')
            # print(user.verify_password(form.password.data))
            return render_template('index.html',
                                   navs=navs,
                                   log_in=user,
                                   footer_l=footer_l_get()
                                   )
        else:
            flash(f"Incorrect input data", category='danger')
    return render_template('login.html',
                           form=form,
                           navs=navs,
                           footer_l=footer_l_get())


@app.route('/logout')
def logout():
    logout_user()
    flash(f"You have been logged out", category='success')
    return redirect(url_for("home"))


@app.route('/users')
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


@app.route('/account')
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


if __name__ == '__main__':
    app.run(debug=True)
