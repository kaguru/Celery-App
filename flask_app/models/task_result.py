from sqlalchemy import Column, Integer, String, DateTime, Index

from ..db import db_engine
from ..common import common_model

seq = db_engine.Sequence('task_results_id_seq')


class TaskResult(db_engine.Model, common_model.CommonModel):
    __tablename__ = 'task_results'
    __table_args__ = (
        Index('task_results_index', "result", "created_at"),)
    id = Column(Integer(), seq, server_default=seq.next_value(), primary_key=True)
    result = Column(String(10000))
    created_at = Column(DateTime(timezone=True))

    def __repr__(self):
        return '<TaskResult %r>' % id