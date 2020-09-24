from celery import Celery

app = Celery('tasks', backend='redis://localhost', broker='pyamqp://admin:pass@localhost//')


@app.task
def add(x, y):
    return x + y
