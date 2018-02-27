from rest_framework import serializers

from magsoft_api.models import Alerts


class AlertCreationSerializer(serializers.ModelSerializer):
    location = serializers.CharField(max_length=255, required=False)

    class Meta:
        model = Alerts
        fields = ('email', 'title', 'text', 'location')
