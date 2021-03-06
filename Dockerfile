FROM ubuntu_18_pipenv_celery:latest

WORKDIR /

COPY ./requirements.txt /requirements.txt
RUN pip install -r requirements.txt
RUN pip install flower

COPY ./flask_app /flask_app
COPY ./supervisord_add.conf supervisord_add.conf
COPY ./supervisord_divide.conf supervisord_divide.conf

CMD ["gunicorn", "-k", "gevent", "-w", "1", "--log-level", "debug", "-b", "0.0.0.0:5000", "flask_app:create_app()"]

EXPOSE 5000
