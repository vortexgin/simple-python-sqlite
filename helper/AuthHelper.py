from exception import NotAuthorizedException


def is_auth(user):
    if user is False:
        raise NotAuthorizedException(message="Unauthorized")

    return True
