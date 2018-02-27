from rest_framework import serializers

from magsoft_api import pass_hash


class PasswordField(serializers.CharField):
    def get_value(self, obj):
        return obj #Use the whole object when trying to get the internal value for this field

    # When getting the internal value for this field, hash the password - we'll get it as
    # plain text, but want it stored as a hashed password.
    def to_internal_value(self, obj):
        return pass_hash(obj['email'], obj['password'])
