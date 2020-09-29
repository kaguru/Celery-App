from flask import g, current_app
from celery import Celery

from flask_app import create_app

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

    db_host = os.environ['DB_HOST']
    db_port = os.environ['DB_PORT']
    db_username = os.environ['DB_USERNAME']
    db_password = os.environ['DB_PASSWORD']
    db_name = os.environ['DB_NAME']

    redis_url = os.environ['REDIS_URL']
    rabbit_mq_url = os.environ['RABBIT_MQ_URL']

    celery = Celery(app.import_name,
                    backend=redis_url,
                    broker=rabbit_mq_url,
                    include=CELERY_TASK_LIST)
    celery.conf.update(app.config)
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
        print(f"{'*'*70}\ng.celery_instance::{g.celery_instance}\n{'*'*70}")
        return g.celery_instance
    celery_new_instance = create_celery_app()
    print(f"{'*' * 70}\ncelery_instance::{celery_new_instance}\n{'*' * 70}")
    return celery_new_instance



