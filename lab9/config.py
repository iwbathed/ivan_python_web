import os


main_dir = os.path.abspath(os.path.dirname(__file__))

SECRET_KEY = 'qw5er6643fg53f43t'
WTF_CSRF_ENABLED = True

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + \
                          os.path.join(main_dir, 'site.db')

SQLALCHEMY_TRACK_MODIFICATIONS = False


class Config:
    DEVELOPMENT = False
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'mysupersecretkey'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = True

class DevConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI') or \
                              'sqlite:///' + os.path.join(main_dir, 'site.db')

class TestConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(main_dir, 'test_site.db')

class ProdConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI') or \
                              'sqlite:///' + os.path.join(main_dir, 'site.db')

config = {
    'dev': DevConfig,
    'prod': ProdConfig,
    'default': DevConfig,
    'test': TestConfig,
}