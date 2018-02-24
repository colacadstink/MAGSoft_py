import inspect
from django.http import HttpResponse
from rest_framework.exceptions import AuthenticationFailed, NotAuthenticated


def auth_required(func):
    args_list = inspect.getfullargspec(func)[0]
    request_index = args_list.index("request")

    def wrapper(*args):
        request = args[request_index]
        if request.user.is_authenticated:
            return func(*args)
        else:
            raise NotAuthenticated(detail="You must be logged in to do this.")
    return wrapper


def staff_required(func):
    args_list = inspect.getfullargspec(func)[0]
    request_index = args_list.index("request")

    def wrapper(*args):
        request = args[request_index]
        if request.user.is_authenticated:
            if request.user.is_staff:
                return func(*args)
            else:
                raise AuthenticationFailed(detail="You must be an admin to do this.")
        else:
            raise NotAuthenticated(detail="You must be logged in to do this.")
    return wrapper
