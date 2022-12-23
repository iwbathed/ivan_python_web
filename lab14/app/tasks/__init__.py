from flask import Blueprint

todo_bp = Blueprint('task', __name__, url_prefix='/task',
                    template_folder='templates/tasks')

from . import views




