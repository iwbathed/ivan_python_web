import os


main_dir = os.path.abspath(os.path.dirname(__file__))

SECRET_KEY = '123141241231231241421'
WTF_CSRF_ENABLED = True

SQLALCHEMY_DATABASE_URI = "postgresql:///flask_database_thws_user:BOP1T8jskuFImmj7MksNYdlpRHiOeg2l@dpg-cekq9fla4991ihi2dbk0-a/flask_database_thws"
# 'postgresql:///' + os.path.join(main_dir, 'site.db')

SQLALCHEMY_TRACK_MODIFICATIONS = True


class Config:
    DEVELOPMENT = True
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'mysupersecretkey'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = True



class DevConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    if os.getenv('DATABASE_URL'):
        SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL').replace("postgres://", "postgresql://", 1)
    else:
        SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(main_dir, 'instance', 'app.db')}"

    # SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI') or \
    #                           'postgresql:///' + os.path.join(main_dir, 'site.db')


class TestConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    if os.getenv('DATABASE_URL'):
        SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL').replace("postgres://", "postgresql://", 1)
    else:
        SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(main_dir, 'instance', 'app.db')}"

    # SQLALCHEMY_DATABASE_URI = 'postgresql:///' + os.path.join(main_dir, 'test_site.db')
    WTF_CSRF_ENABLED = False


class ProdConfig(Config):
    if os.getenv('DATABASE_URL'):
        SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL').replace("postgres://", "postgresql://", 1)
    else:
        SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(main_dir, 'instance', 'app.db')}"

    # SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI') or \
    #                           'postgresql:///' + os.path.join(main_dir, 'site.db')


config = {
    'dev': DevConfig,
    'prod': ProdConfig,
    'default': DevConfig,
    'test': TestConfig,
}
