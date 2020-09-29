from flask import current_app
import logging
import os
from logging.handlers import SMTPHandler, RotatingFileHandler
from functools import wraps
import traceback


# CREATE CUSTOME LOGGER
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# SET LOG FILES DESTINATIONS
log_dir = os.path.join(current_app.instance_path, 'log')
os.makedirs(log_dir, exist_ok=True)

# CREATE HANDLERS
file_log_handler = RotatingFileHandler(os.path.join(log_dir, 'error.log'), maxBytes=1000000, backupCount=1)
stream_log_handler = logging.StreamHandler()

# CREATE MAIL HANDLER
mail_log_handler = SMTPHandler(
    mailhost=('smtp.gmail.com', 587),
    fromaddr='lnh123@gmail.com',
    toaddrs='lnh123@gmail.com',
    subject='SCORING ERROR',
    credentials=('lnh123@gmail.com', 'G@cheru123'),
    secure=''
)

# SET FILE, STREAM AN MAIL HANDLER LOG LEVELS
file_log_handler.setLevel(logging.ERROR)
# stream_log_handler.setLevel(logging.WARN)
stream_log_handler.setLevel(logging.DEBUG)
mail_log_handler.setLevel(logging.ERROR)

# SET HANDLERS LOG MESSAGE FORMAT
log_message_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_log_handler.setFormatter(log_message_format)
stream_log_handler.setFormatter(log_message_format)

# ADD HANDLERS TO LOGGER
logger.addHandler(file_log_handler)
logger.addHandler(stream_log_handler)
logger.addHandler(mail_log_handler)


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
                log_message = f'\n{"-" * 50}\nFUNCTION NAME :: {fxn_name}' \
                              f'\nLOCALS ARGS() :: {locals().get("args")}' \
                              f'\nLOCALS KWARGS() :: {locals().get("kwargs")}'
                logger.info(log_message)
                return func(*args, **kwargs)
            except Exception as e:
                tb = traceback.format_exc()
                log_message = f'\n{"-"*50}\nEXCEPT :: \nFUNCTION NAME :: {fxn_name} \nERROR CLASS :: {e.__class__}' \
                              f'\nLOCALS ARGS() :: {locals().get("args")}' \
                              f'\nLOCALS KWARGS() :: {locals().get("kwargs")}' \
                              f'\nTRACEBACK ::  {tb}\n{"-"*50}\n' \
                              f'\nTRACEBACK ::  {e}\n{"-"*50}\n'
                logger.error(log_message)
                return func(*args, **kwargs)
        return wrapped_function
    return exception_function
