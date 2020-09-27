FROM ubuntu_18_pipenv_celery:latest

WORKDIR /

COPY ./flask_app /flask_app
COPY ./requirements.txt /requirements.txt
COPY ./supervisord.conf supervisord.conf

RUN pip install -r requirements.txt

CMD ["gunicorn", "-k", "gevent", "-w", "1", "--log-level", "debug", "-b", "0.0.0.0:5000", "flask_app:create_app()"]

EXPOSE 5000