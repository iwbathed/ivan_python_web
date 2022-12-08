from flask import Blueprint

account_bp = Blueprint('account', __name__, url_prefix='/',
                        template_folder='templates/account')

from . import views
