
# -*- coding: UTF-8 -*-
"""
hello_flask: First Python-Flask webapp
"""
import platform
from datetime import datetime

import logging
from flask import Flask, render_template, request, \
    redirect, url_for, flash, session
from app.forms import Form
from app import app, db
from app.models import Person

logging.basicConfig(filename='app.log', filemode='a',
                    format='%(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

#app = Flask(__name__)

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
    return render_template('index.html',
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
    if request.method == 'GET':
        return render_template('contact.html', navs=navs,
                               contact_l=contact_l,
                               footer_l=footer_l_get(),
                               form=form,
                               session=session)
    if form.validate_on_submit():
        username = form.name.data
        email = form.email.data

        session['name'] = username
        session['email'] = email

        contact_info = Person(name=username, email=email)
        db.session.add(contact_info)
        db.session.commit()

        form.name.data = 'Successfull validate '
        flash(f"Data sent successfully : {username} {email}",
              category='success')
        logging.info(f"Data sent successfully : {username} {email}")
        return redirect(url_for("contact"))

    flash("Not validate (Post)", category='warning')
    logging.warning("Not validate (Post)")
    return redirect(url_for("contact"))



@app.route('/projects')
def projects():

    return render_template('projects.html',
                           navs=navs,
                           footer_l=footer_l_get())

@app.route('/person_info', methods=['GET'])
def person_info():
    user_contact_id = request.args.get('id')
    if user_contact_id:
        contact_info_list = Person.query.filter_by(id=user_contact_id)
    else:
        contact_info_list = Person.query.all()
    return render_template('person.html', contact_info_list=contact_info_list)


@app.route('/person/delete/<id>')
def delete_person(id):
    Person.query.filter_by(id=id).delete()
    try:
        db.session.commit()
    except:
        db.session.flush()
        db.session.rollback()
    return "<h3>Deleted!</h3>"



if __name__ == '__main__':
    app.run(debug=True)