
from app import db, bcrypt


class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20), unique=False, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    phone = db.Column(db.String(15), unique=True, nullable=False)
    subject = db.Column(db.String(30), unique=False, nullable=False)
    message = db.Column(db.Text, unique=False, nullable=False)


class User(db.Model):
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

