from . import db


class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20), unique=False, nullable=False)
    email = db.Column(db.String(225), unique=True, nullable=False)
    phone = db.Column(db.String(15), unique=True, nullable=False)
    subject = db.Column(db.String(30), unique=False, nullable=False)
    message = db.Column(db.Text, unique=False, nullable=False)

    def repr(self):
        return f"Name : {self.name}, Email: {self.email}, Phone: {self.phone}, Subject: {self.subject},  Message: {self.message}"
