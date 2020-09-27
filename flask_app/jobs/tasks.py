from ..celery_instance import get_celery_instance


celery = get_celery_instance()


@celery.task
def add(x, y):
    return x + y