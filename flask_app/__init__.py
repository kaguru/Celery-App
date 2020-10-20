from flask import Flask
from flask_migrate import Migrate

import os

CELERY_TASK_LIST = [
    'flask_app.jobs.tasks',
]


def create_app():
    app = Flask(__name__,
                instance_relative_config=True)
    app.config['SECRET_KEY'] = os.environ['SECRET_KEY']
    app.config['DEBUG'] = True
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # DATABASES CONFIGS
    db_host = os.environ['DB_HOST']
    db_port = os.environ['DB_PORT']
    db_username = os.environ['DB_USERNAME']
    db_password = os.environ['DB_PASSWORD']
    db_name = os.environ['DB_NAME']

    app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql+psycopg2://{db_username}:{db_password}@{db_host}/{db_name}'

    with app.app_context():
        from .celery_instance import set_celery_instance
        from .redis_instance import set_redis_instance

        set_celery_instance(app)
        set_redis_instance()

        from .ma import ma
        from .db import init_app_db, db_engine
        from .models import create_tables
        from .resources import bp_home

        ma.init_app(app)
        init_app_db(app)
        Migrate(app, db_engine)
        app.register_blueprint(bp_home)
    return app


if __name__ == "__main__":
    app = create_app()
    app.run()
