from flask import Blueprint

contact_bp = Blueprint('contact', __name__, url_prefix='/',
                        template_folder='templates/contact')

from . import views