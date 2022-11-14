
# -*- coding: UTF-8 -*-

import platform
from datetime import datetime

import logging
from flask import Flask, render_template, request, \
    redirect, url_for, flash, session
from app.forms import Form, RegistrationForm, LoginForm
from app import app, db, bcrypt
from app.models import Person, User

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
        "name": "Log in",
        "url": "login"
    },
    {
        "name": "Register",
        "url": "register"
    },
    {
        "name": "Users",
        "url": "users"
    }

]


def footer_l_get():
    return [platform.platform(),
              request.headers.get('User-Agent'),
              datetime.now()
              ]


@app.route('/')
def start():
    return redirect("/home")


@app.route('/home')
def home():
    log_in = False;
    return render_template('index.html',
                           log_in=log_in,
                           navs=navs,
                           footer_l=footer_l_get())


@app.route('/about')
def about():
    return render_template('about.html',
                           navs=navs,
                           footer_l=footer_l_get())


@app.route('/contact', methods=['GET', 'POST'])
def contact():
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

            form.name.data = 'Successfull validate '
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
                           contact_l=contact_l,
                           footer_l=footer_l_get(),
                           form=form,
                           session=session)



    flash("Not validate (Post)", category='warning')
    logging.warning("Not validate (Post)")
    return redirect(url_for("contact"))


@app.route('/projects')
def projects():
    return render_template('projects.html',
                           navs=navs,
                           footer_l=footer_l_get())



@app.route('/person_info', methods=['GET'])
def persons_info():
    contact_info_list = Person.query.all()
    return render_template('person.html',
                           contact_info_list=contact_info_list,
                           navs=navs,
                           footer_l=footer_l_get()
                           )


@app.route('/person_info/<id>', methods=['GET'])
def person_info(id):
    contact_info_list = Person.query.filter_by(id=id)
    return render_template('person.html',
                           contact_info_list=contact_info_list,
                           navs=navs,
                           footer_l=footer_l_get()
                           )

@app.route('/person/delete/<id>')
def delete_person(id):

    try:
        Person.query.filter_by(id=id).delete()
        db.session.commit()
    except:
        db.session.flush()
        db.session.rollback()
    return render_template('on_delete.html',
                           id=id,
                           navs=navs,
                           footer_l=footer_l_get()
                           )


@app.route('/register', methods=['GET', 'POST'])
def register():
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
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        user = User.query.filter_by(email=email).first()


        if user and user.verify_password(form.password.data):
            print(user.verify_password(form.password.data))
            return render_template('index.html',
                                   form=form,
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



@app.route('/users')
def users():
    all_users = User.query.all()
    return render_template('users.html',
                           all_users=all_users,
                           navs=navs,
                           footer_l=footer_l_get()
                           )


if __name__ == '__main__':
    app.run(debug=True)