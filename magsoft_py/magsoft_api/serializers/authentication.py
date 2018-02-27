from rest_framework import serializers

from magsoft_api.models import Alerts, Users, Settings


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
