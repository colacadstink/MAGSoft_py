from magsoft_api.models import Users

import hashlib


class UserBackend:
    def authenticate(self, request, username=None, password=None):
        db_password = hashlib.sha512((username + password).encode("utf-8")).hexdigest()
        user = None
        try:
            user = Users.objects.get(email=username, password=db_password)
        except Users.DoesNotExist:
            return None
        return user

    def get_user(self, email):
        try:
            return Users.objects.get(email=email)
        except Users.DoesNotExist:
            return None
