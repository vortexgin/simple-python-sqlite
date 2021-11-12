from . import BaseException


class NotAuthorizedException(BaseException):
    message = "You're not authorized"
    status_code = 401
