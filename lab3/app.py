# # -*- coding: UTF-8 -*-
# """
# hello_flask: First Python-Flask webapp
# """
# from flask import Flask  # From module flask import class Flask
# app = Flask(__name__)    # Construct an instance of Flask class for our webapp
#
# @app.route('/')   # URL '/' to be handled by main() route handler
# def main():
#     """Say hello"""
#     return 'Hello, world!'
#
# if __name__ == '__main__':  # Script executed directly?
#     app.run()  # Launch built-in web server and run this Flask webapp




# -*- coding: UTF-8 -*-
"""
hello_flask: First Python-Flask webapp
"""
import os
import platform
from datetime import datetime
# import request

from flask import Flask, render_template, request, redirect, url_for
app = Flask(__name__)




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





@app.route('/')
def start():
    return redirect("/home")


@app.route('/home')
def home():

    footer_l=[platform.platform(),
              request.headers.get('User-Agent'),
              datetime.now()
              ]
    return render_template('index.html', navs=navs, footer_l=footer_l)

@app.route('/about')
def about():
    footer_l = [platform.platform(),
                request.headers.get('User-Agent'),
                datetime.now()
                ]
    return render_template('about.html', navs=navs, footer_l=footer_l)

@app.route('/contact')
def contact():
    footer_l = [platform.platform(),
                request.headers.get('User-Agent'),
                datetime.now()
                ]
    return render_template('contact.html', navs=navs, footer_l=footer_l)

@app.route('/projects')
def projects():
    footer_l = [platform.platform(),
                request.headers.get('User-Agent'),
                datetime.now()
                ]
    return render_template('projects.html', navs=navs, footer_l=footer_l)




# @app.route('/for')
# def fort():
#     user = "admin"
#     return render_template('for_test.html', title="Home", user=user, posts=posts)


# @app.route('/main/<string:name>/<int:n>')
# def home_view(name,n):
#     print(name, n)
#     return render_template('hello.html', name=name, n=n)
#
# @app.route('/re')
# def re():
#     return redirect(url_for('home_view', name = "ivan", n=10, _external=True))
#     #return redirect(url_for('main', page = 11)) #hello/?page=11
#     #return redirect(url_for('fort'))
#
# @app.route('/hello')
# def main():
#     """Say hello"""
#     p = request.args.get("page", 0)
#     return f'Hello, p={p}!'
#
# @app.route('/if')
# def ift():
#     user = "admin"
#     return render_template('if_test.html', title="Home", user=user)

if __name__ == '__main__':
    app.run(debug=True)




#Windows Command Prompt:
#set FLASK_DEBUG=1
#set FLASK_APP=app.py
#set FLASK_ENV=development




