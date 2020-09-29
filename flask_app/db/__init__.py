from flask import current_app, g
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.pool import QueuePool
from ..helpers.log_handler import exception_handler


SQLALCHEMY_ENGINE_OPTIONS = {
    'pool': QueuePool,
    'pool_size': 20,
    'pool_recycle': 120,
    'pool_pre_ping': True,
    'connect_timeout': 500,
    'echo': False
}


db_engine = SQLAlchemy(current_app, SQLALCHEMY_ENGINE_OPTIONS)
raw_db_connection = db_engine.engine.raw_connection()


@exception_handler()
def get_db_session():
    if "db_session" not in g:
        g.db = db_engine.session
    return g.db


@exception_handler()
def close_db(e=None):
    db = g.pop("db_session", None)
    if db is not None:
        db.close()


@exception_handler()
def init_app_db(app):
    app.teardown_appcontext(close_db)
