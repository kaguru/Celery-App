from flask import g
import redis
import os

redis_url = os.environ['REDIS_URL']
redis_port = os.environ['REDIS_PORT']


def set_redis_instance():
    if g:
        if "redis_instance" not in g:
            redis_instance = redis.Redis(host="localhost", port=redis_port, db=0)
            g.redis_instance = redis_instance


def get_redis_instance():
    if g:
        if "redis_instance" not in g:
            set_redis_instance()
        return g.redis_instance
    else:
        return redis.Redis(host="localhost", port=redis_port, db=0)


