def field_required(field_name=None):
    _response = {"status": "error",
                 "message": f"{field_name} field is required"}
    return _response, 400