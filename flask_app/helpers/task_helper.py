from ..redis_instance import get_redis_instance

redis_instance = get_redis_instance()


def only_one(function=None, key="", timeout=None):
    """Enforce only one celery task at a time."""

    def _dec(run_func):

        def _caller(*args, **kwargs):
            ret_value = None
            have_lock = False
            lock = redis_instance.lock(key, timeout=timeout)
            try:
                have_lock = lock.acquire(blocking=False)
                if have_lock:
                    ret_value = run_func(*args, **kwargs)
            finally:
                if have_lock:
                    lock.release()

            return ret_value

        return _caller

    return _dec(function) if function is not None else _dec