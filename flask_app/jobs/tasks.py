from ..celery_instance import get_celery_instance
from ..helpers.task_helper import only_one

celery = get_celery_instance()


@celery.task(name="celery_tasks.tasks.add", default_retry_delay=300, max_retries=5)
@only_one(key="SingleTask", timeout=60 * 5)
def add(x, y):
    """
    Run a Single Task with a timeout of 5 Minutes after which the lock expires
    :param x:
    :param y:
    :return:
    """
    try:
        return x + y
    except Exception as e:
        return
