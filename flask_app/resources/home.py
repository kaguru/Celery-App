from flask import Blueprint


bp = Blueprint('home', __name__, url_prefix='/')


@bp.route("", methods=["GET", "POST"])
def index():
    return "CELERY TASKS APP"
