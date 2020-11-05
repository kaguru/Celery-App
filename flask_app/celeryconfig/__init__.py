from kombu import Queue, Exchange

CELERY_QUEUES = (
    Queue('default', Exchange('default'), routing_key='default'),
    Queue('queue_add', Exchange('exchange_add'), routing_key='tasks_add'),
    Queue('queue_divide', Exchange('exchange_divide'), routing_key='tasks_divide'),
)


CELERY_ROUTES = {
    'tasks_add': {'queue': 'queue_add', 'routing_key': 'tasks_add'},
    'tasks_divide': {'queue': 'queue_divide', 'routing_key': 'tasks_divide'},
}
