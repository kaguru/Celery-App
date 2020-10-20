from flask import Blueprint
from ..jobs import tasks
from ..models import TaskResult
from ..helpers.log_handler import logger

from ..redis_instance import get_redis_instance

import os
import time
from datetime import datetime

redis_url = os.environ['REDIS_URL']

bp = Blueprint('home', __name__, url_prefix='/')

redis_instance = get_redis_instance()


@bp.route("", methods=["GET", "POST"])
def index():
    return "CELERY TASKS APP"


@bp.route("add", methods=["GET", "POST"])
def add_resource():
    result = tasks.add.apply_async(queue='for_task_A', kwargs={"x": 4, "y": 9})
    result_is_ready_before_get = result.ready()
    result_get = result.get()
    result_is_ready_after_get_ready = result.ready()

    TaskResult.create(result=result_get)

    return f"""
        redis_url:: {redis_url}
        <br>
        RESULT:: {result}
        <br>
        RESULT IS READY BEFORE GET:: {result_is_ready_before_get}
        <br>
        RESULT GET:: {result_get}
        <br>
        RESULT IS READY AFTER GET:: {result_is_ready_after_get_ready}
        """


@bp.route("lock/<string:key>", methods=["GET", "POST"])
def lock_resource(key):
    have_lock = False
    my_lock = redis_instance.lock(key, timeout=30)
    try:
        have_lock = my_lock.acquire(blocking=False)
        if have_lock:
            logger.info(f"INSIDE TRY [HAS A LOCK] : BEFORE SLEEPING : {datetime.now()}")
            time.sleep(25)
            logger.info(f"INSIDE TRY [HAS A LOCK] : AFTER SLEEPING : {datetime.now()}")
        else:
            logger.info(f"INSIDE TRY [HAS NOT ACQUIRED A LOCK]")
    except Exception as e:
        logger.info(f"INSIDE EXCEPT [HAS NOT ACQUIRED A LOCK]")
    finally:
        if have_lock:
            logger.info(f"INSIDE FINALLY [HAS A LOCK] BEFORE RELEASE")
            my_lock.release()
            logger.info(f"INSIDE FINALLY [HAS NOT ACQUIRED A LOCK] AFTER RELEASE")
        else:
            logger.info(f"INSIDE FINALLY [HAS NOT ACQUIRED A LOCK]")
        return f"{'LOCK ACQUIRED for '+key if have_lock else 'UNABLE TO ACQUIRE A LOCK for '+key }"


@bp.route("test-redis", methods=["GET", "POST"])
def test_redis_resource():
    redis_instance.set("foo", "bar")

    return f"""
        redis_url:: {redis_url}
        <br>
        FOO:: {redis_instance.get('foo')}
        """

