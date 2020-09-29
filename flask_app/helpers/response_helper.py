from collections import OrderedDict


def success_response(data=None, message=None, status_code=None):
    response_dict = message_builder(data=data, message=message, success=True)
    return response_dict, status_code if status_code else 200


def success_response_v2(data=None, message=None, status_code=None):
    # response_dict = message_builder(data=data, message=message, success=True)
    return data, status_code if status_code else 200


def error_response(message, status_code=None):
    response_dict = message_builder(message=message, success=False)
    return response_dict, status_code if status_code else 400


def message_builder(data=None, message=None, success=False):
    response_dict = OrderedDict()
    # response_dict["status"] = "success" if success else "error"
    response_dict["success"] = True if success else False
    if success:
        if data:
            response_dict["data"] = data
        if message:
            response_dict["message"] = message
    else:
        response_dict["message"] = message
    return dict(response_dict)
