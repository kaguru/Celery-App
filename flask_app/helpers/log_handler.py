from flask import current_app
import logging
import os
from logging.handlers import RotatingFileHandler
from functools import wraps
import traceback
from flask_app.helpers.time_helper import get_current_kenya_time_utc

# CREATE CUSTOME LOGGER
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# SET LOG FILES DESTINATIONS
# logs_dir = os.path.join(current_app.instance_path, 'log')
log_dir = 'logs'
os.makedirs(log_dir, exist_ok=True)

# CREATE HANDLERS
file_log_handler = RotatingFileHandler(os.path.join(log_dir, 'error.log'), maxBytes=1000000, backupCount=1)
stream_log_handler = logging.StreamHandler()


# SET FILE, STREAM LOG LEVELS
file_log_handler.setLevel(logging.WARN)
# stream_log_handler.setLevel(logging.WARN)
stream_log_handler.setLevel(logging.DEBUG)

# SET HANDLERS LOG MESSAGE FORMAT
log_message_format = logging.Formatter(f"\n{'-'*100}\n%(asctime)s - %(name)s - %(levelname)s - %(message)s\n{'-'*100}\n")
file_log_handler.setFormatter(log_message_format)
stream_log_handler.setFormatter(log_message_format)

# ADD HANDLERS TO LOGGER
logger.addHandler(file_log_handler)
logger.addHandler(stream_log_handler)


# RETURN LOGGER
def get_logger():
    return logger


# RETURN EXCEPTION HANDLER
def exception_handler():
    def exception_function(func):
        fxn_name = func.__name__
        @wraps(func)
        def wrapped_function(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                log_message = get_formatted_log_message(e, *args, fxn_name, **kwargs)
                logger.error(log_message)
                return func(*args, **kwargs)
        return wrapped_function
    return exception_function


def get_formatted_log_message(e, function_name, *args, **kwargs):
    return f"""
            FUNCTION NAME :: {function_name}
            EXCEPTION CLASS :: {e.__class__}
            ARGS :: {locals().get("args")}
            KWARGS :: {locals().get("kwargs")}
            TIME :: {get_current_kenya_time_utc()}
            TRACEBACK ::  {traceback.format_exc()}\n{"-"*50}
            """
