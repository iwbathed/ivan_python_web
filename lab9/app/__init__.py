from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_login import LoginManager


from config import config

# app = Flask(__name__)
# app.config.from_object("config")
# db = SQLAlchemy(app)
# migrate = Migrate(app, db)
# bcrypt = Bcrypt(app)
# login_manager = LoginManager(app)
# login_manager.login_view = 'login'
# login_manager.message_category = 'info'

db = SQLAlchemy()
bcrypt = Bcrypt()
migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = "account.login"
login_manager.login_message_category = "info"


# from .account import account_bp
# from .contact import contact_bp
# from .home import home_bp

# app.register_blueprint(account_bp)
# app.register_blueprint(contact_bp)
# app.register_blueprint(home_bp)


def create_app(config_name = 'default'):
    app = Flask(__name__)
    app.config.from_object(config.get(config_name))

    db.init_app(app)
    migrate.init_app(app, db, render_as_batch=True)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    with app.app_context():
        from app.home import home_bp
        from app.contact import contact_bp
        from app.account import account_bp

        app.register_blueprint(home_bp)
        app.register_blueprint(contact_bp)
        app.register_blueprint(account_bp)

    return app



