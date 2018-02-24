import hashlib

from rest_framework.exceptions import APIException


def pass_hash(username, password):
    return hashlib.sha512((username + password).encode("utf-8")).hexdigest()


class CustomAPIException(APIException):
    def __init__(self, status, details):
        self.status_code = status
        self.detail = details
