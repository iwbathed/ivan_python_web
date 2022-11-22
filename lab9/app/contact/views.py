from flask import render_template, session, flash, redirect, url_for, request
# from flask_login import login_required
from .. import db
from flask_login import login_user, current_user, logout_user, login_required


import platform
from datetime import datetime

from app.models import Person, User
from .forms import Form
from . import contact_bp



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


@contact_bp.route('/contact', methods=['GET', 'POST'])
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

            return redirect(url_for("contact"))
        flash("Not validate (Post)", category='warning')

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

@contact_bp.route('/person_info', methods=['GET'])
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


@contact_bp.route('/person_info/<id>', methods=['GET'])
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

@contact_bp.route('/person/delete/<id>')
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