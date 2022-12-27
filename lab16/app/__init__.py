from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_ckeditor import CKEditor
import sqlalchemy as sa
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
    register_cli_commands(app)

    with app.app_context():
        from app.home import home_bp
        from app.contact import contact_bp
        from app.account import account_bp
        from app.tasks import todo_bp
        from app.category_api import api_bp
        from app.tasks_api import api2_bp
        from app.swagger import swagger_bp
        from app.admin import create_module

        admin = create_module(db)
        admin.init_app(app)

        app.register_blueprint(home_bp)
        app.register_blueprint(contact_bp)
        app.register_blueprint(account_bp)
        app.register_blueprint(todo_bp)
        app.register_blueprint(api_bp)
        app.register_blueprint(api2_bp)
        app.register_blueprint(swagger_bp)

        engine = sa.create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
        inspector = sa.inspect(engine)
        if not inspector.has_table("user"):
            with app.app_context():
                db.drop_all()
                db.create_all()
                app.logger.info('Initialized the database!')
        else:
            app.logger.info('Database already contains the users table.')
    return app


def register_cli_commands(app):
    @app.cli.command('init_db')
    def initialize_database():
        """Initialize the database."""
        db.drop_all()
        db.create_all()
        # echo('Initialized the database!')





