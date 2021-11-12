from . import BaseException


class NotFoundException(BaseException):
    message = "Entity not found"
    status_code = 404
