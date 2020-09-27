from flask import Flask
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

    with app.app_context():
        from .celery_instance import set_celery_instance
        set_celery_instance(app)

        from .ma import ma
        from .resources import bp_home

        ma.init_app(app)

        app.register_blueprint(bp_home)
    return app


if __name__ == "__main__":
    app = create_app()
    app.run()
