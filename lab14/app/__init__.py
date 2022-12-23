from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_ckeditor import CKEditor

from config import config


ckeditor = CKEditor()
db = SQLAlchemy()
bcrypt = Bcrypt()
migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = "account.login"
login_manager.login_message_category = "info"
SECRET_KEY = None

def create_app(config_name = 'default'):
    app = Flask(__name__)
    app.config.from_object(config.get(config_name))

    global SECRET_KEY
    SECRET_KEY = app.secret_key
    db.init_app(app)
    migrate.init_app(app, db, render_as_batch=True)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    ckeditor.init_app(app)

    with app.app_context():
        from app.home import home_bp
        from app.contact import contact_bp
        from app.account import account_bp
        from app.tasks import todo_bp
        from app.category_api import api_bp
        from app.tasks_api import api2_bp
        from app.swagger import swagger_bp

        app.register_blueprint(home_bp)
        app.register_blueprint(contact_bp)
        app.register_blueprint(account_bp)
        app.register_blueprint(todo_bp)
        app.register_blueprint(api_bp)
        app.register_blueprint(api2_bp)
        app.register_blueprint(swagger_bp)

    return app



