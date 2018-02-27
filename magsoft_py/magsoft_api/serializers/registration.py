from rest_framework import serializers

from magsoft_api.models import Users
from magsoft_api.serializers import PasswordField


class UserSerializer(serializers.ModelSerializer):
    password = PasswordField()

    class Meta:
        model = Users
        fields = ('email', 'password', 'first_name', 'last_name', 'phone', 'emergencyname', 'emergencyphone', 'dob')
