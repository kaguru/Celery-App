from flask import Blueprint
from ..jobs import tasks
from ..models import TaskResult

bp = Blueprint('home', __name__, url_prefix='/')


@bp.route("", methods=["GET", "POST"])
def index():
    return "CELERY TASKS APP"


@bp.route("add", methods=["GET", "POST"])
def add_resource():
    result = tasks.add.delay(4, 4)
    result_is_ready_before_get = result.ready()
    result_get = result.get()
    result_is_ready_after_get_ready = result.ready()

    TaskResult.create(result=result_get)

    return f"""
        RESULT:: {result}
        RESULT IS READY BEFORE GET:: {result_is_ready_before_get}
        RESULT GET:: {result_get}
        RESULT IS READY AFTER GET:: {result_is_ready_after_get_ready}
        """

