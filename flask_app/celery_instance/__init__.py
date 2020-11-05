from flask import g, current_app
from celery import Celery

from flask_app import create_app
from flask_app import celeryconfig

import os

CELERY_TASK_LIST = [
    'flask_app.jobs.tasks',
]


def create_celery_app(_app=None):
    """
    Create a new Celery object and tie together the Celery config to the app's
    config. Wrap all tasks in the context of the application.

    :param app: Flask app
    :return: Celery app
    """
    app = create_app() if not _app else _app

    redis_url = os.environ['REDIS_URL']
    redis_port = os.environ['REDIS_PORT']
    rabbit_mq_url = os.environ['RABBIT_MQ_URL']

    celery = Celery(app.import_name,
                    backend=f"{redis_url}",
                    broker=rabbit_mq_url,
                    include=CELERY_TASK_LIST)
    celery.config_from_object(celeryconfig)
    celery.conf.update(app.config)
    celery.conf.task_create_missing_queues = True
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)
    celery.Task = ContextTask
    return celery


def set_celery_instance(app=None):
    if "celery_instance" not in g:
        g.celery_instance = create_celery_app(_app=app)


def get_celery_instance():
    if g:
        if "celery_instance" not in g:
            g.celery_instance = create_celery_app()
        return g.celery_instance
    celery_new_instance = create_celery_app()
    return celery_new_instance



