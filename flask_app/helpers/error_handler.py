from flask import current_app
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError, ProgrammingError

from ..helpers.response_helper import error_response


NOT_FOUND_ERROR_MESSAGE = "{item} not found"
NOT_CREATED_ERROR_MESSAGE = "unable to create {item}"
NOT_UPDATED_MESSAGE = "unable to update {item}"
NOT_DELETED_MESSAGE = "unable to delete {item}"
DEFAULT_ERROR_MESSAGE = "An Error Occurred"


def init_error_handler():
    @current_app.errorhandler(ValidationError)
    def marshmallow_error_handler(error):
        print(f"****** Exception marshmallow_error_handler()\n {error}")
        return error_response(message=error.messages, status_code=400)

    @current_app.errorhandler(IntegrityError)
    def integrity_error_handler(error):
        print(f"****** Exception integrity_error_handler()\n {error}")
        return error_response(message="integrity error occurred", status_code=400)

    @current_app.errorhandler(ProgrammingError)
    def program_error_handler(error):
        print(f"****** Exception program_error_handler() \n {error}\n")
        return error_response(message="error occurred", status_code=400)


def abort_if_none(item, error_message):
    received_error = error_message.format(item=item).format(item=item)
    if received_error in [NOT_FOUND_ERROR_MESSAGE.format(item=item),
                          NOT_UPDATED_MESSAGE.format(item=item),
                          NOT_DELETED_MESSAGE.format(item=item)]:
        return error_response(message=error_message.format(item=item), status_code=404)
    else:
        return error_response(message=error_message.format(item=item), status_code=400)


def abort_unauthenticated():
    message = "Sorry you are not Authenticated"
    return error_response(message=message, status_code=401)
