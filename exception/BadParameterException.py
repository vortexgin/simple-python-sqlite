from . import BaseException


class BadParameterException(BaseException):
    message = "Missing data for required fields"
    status_code = 400
