import os


main_dir = os.path.abspath(os.path.dirname(__file__))

SECRET_KEY = '123141241231231241421'
WTF_CSRF_ENABLED = True

SQLALCHEMY_DATABASE_URI = 'postgresql:///' + \
                          os.path.join(main_dir, 'site.db')

SQLALCHEMY_TRACK_MODIFICATIONS = True


class Config:
    DEVELOPMENT = True
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'mysupersecretkey'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = True



class DevConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI') or \
                              'postgresql:///' + os.path.join(main_dir, 'site.db')


class TestConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgresql:///' + os.path.join(main_dir, 'test_site.db')
    WTF_CSRF_ENABLED = False


class ProdConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI') or \
                              'postgresql:///' + os.path.join(main_dir, 'site.db')


config = {
    'dev': DevConfig,
    'prod': ProdConfig,
    'default': DevConfig,
    'test': TestConfig,
}
