from .task_result import TaskResult
from ..db import db_engine


def create_tables():
    db_engine.create_all()