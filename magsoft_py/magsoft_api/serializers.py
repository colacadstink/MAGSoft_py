from rest_framework import serializers

from magsoft_api import pass_hash
from magsoft_api.models import Users, Settings, Alerts


class PasswordField(serializers.CharField):
    def get_value(self, obj):
        return obj #Use the whole object when trying to get the internal value for this field

    # When getting the internal value for this field, hash the password - we'll get it as
    # plain text, but want it stored as a hashed password.
    def to_internal_value(self, obj):
        return pass_hash(obj['email'], obj['password'])


class AlertsForUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alerts
        fields = ('id', 'title', 'text', 'location')


class WhoAmISerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ('email', 'canroom', 'is_staff', 'alerts', 'cur_year')

    alerts = serializers.SerializerMethodField()
    cur_year = serializers.SerializerMethodField()

    def get_cur_year(self, obj):
        return Settings.objects.get(key='curYear').value

    def get_alerts(self, obj):
        queryset = Alerts.objects.filter(email=obj.email)
        return AlertsForUserSerializer(queryset, many=True).data


class UserSerializer(serializers.ModelSerializer):
    password = PasswordField()

    class Meta:
        model = Users
        fields = ('email', 'password', 'first_name', 'last_name', 'phone', 'emergencyname', 'emergencyphone', 'dob')


class AlertCreationSerializer(serializers.ModelSerializer):
    location = serializers.CharField(max_length=255, required=False)

    class Meta:
        model = Alerts
        fields = ('email', 'title', 'text', 'location')
