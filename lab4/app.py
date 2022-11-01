
# -*- coding: UTF-8 -*-
"""
hello_flask: First Python-Flask webapp
"""
import os
import platform
from datetime import datetime
# import request
import logging
from flask import Flask, render_template, request, \
    redirect, url_for, flash, session
from forms import Form
logging.basicConfig(filename='app.log', filemode='a',
                    format='%(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

app = Flask(__name__)

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



if __name__ == '__main__':
    app.run(debug=True)


