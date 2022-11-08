import os


main_dir = os.path.abspath(os.path.dirname(__file__))

SECRET_KEY = 'qw5er6643fg53f43t'
WTF_CSRF_ENABLED = True

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + \
                          os.path.join(main_dir, 'site.db')

SQLALCHEMY_TRACK_MODIFICATIONS = False

