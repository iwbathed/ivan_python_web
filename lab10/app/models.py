
from app import db, bcrypt, login_manager
from flask_login import UserMixin


import platform
from flask import request
from datetime import datetime

navs = [
    {
        "name" : "Home",
        "url" : "home.home"
    },
    {
        "name" : "About",
        "url" : "home.about"
    },
    {
        "name": "Projects",
        "url": "home.projects"
    },
    {
        "name": "Contact",
        "url": "contact.contact"
    },
    {
        "name": "Persons info",
        "url": "contact.persons_info"
    },
    {
        "name": "Users",
        "url": "account.users"
    },
    {
        "name": "Tasks",
        "url": "task.user_profile"
    },
    {
        "name": "Log in",
        "url": "account.login"
    },
    {
        "name": "Register",
        "url": "account.register"
    },
]


def footer_l_get():
    return [platform.platform(),
              request.headers.get('User-Agent'),
              datetime.now()
              ]

class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20), unique=False, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    phone = db.Column(db.String(15), unique=True, nullable=False)
    subject = db.Column(db.String(30), unique=False, nullable=False)
    message = db.Column(db.Text, unique=False, nullable=False)



@login_manager.user_loader
def user_loader(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    image = db.Column(db.String(20), nullable=False, default='default.jpg')
    hashed_password = db.Column(db.String(255), nullable=False)

    @property
    def password(self):
        raise AttributeError('Not readable')

    @password.setter
    def password(self, password):
        self.hashed_password = bcrypt.generate_password_hash(password)

    def verify_password(self, password):
        print(self.hashed_password.decode('utf-8'))
        print(password)
        return bcrypt.check_password_hash(self.hashed_password.decode('utf-8'), password)

    def repr(self):
        return f"Name : {self.name}, Email: {self.email}, Phone: {self.phone}, Subject: {self.subject},  Message: {self.message}"

