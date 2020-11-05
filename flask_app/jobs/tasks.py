from flask_app.celery_instance import get_celery_instance
from flask_app.helpers.task_helper import only_one
from flask_app.helpers.log_handler import get_formatted_log_message, get_logger

celery = get_celery_instance()

logger = get_logger()


@celery.task(name="celery_tasks.tasks.add", bind=True, default_retry_delay=5, max_retries=3)
@only_one(key="SingleTask", timeout=60 * 5)
def add(self, x, y):
    """
    Run a Single Task with a timeout of 5 Minutes after which the lock expires
    """
    try:
        return int(x) + int(y)
    except Exception as e:
        return


@celery.task(name="celery_tasks.tasks.divide", bind=True, default_retry_delay=5, max_retries=3)
@only_one(key="SingleTask", timeout=60 * 5)
def divide(self, x, y):
    """
    Run a Single Task with a timeout of 5 Minutes after which the lock expires
    """
    exception = None
    try:
        return int(x) / int(y)
    except Exception as e:
        exception = e
        raise self.retry(exc=e)
    finally:
        if exception:
            formatted_log_message = get_formatted_log_message(exception, 'tasks.divide', x, y)
            logger.critical(formatted_log_message)
