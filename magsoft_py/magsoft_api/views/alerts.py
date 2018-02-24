from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.exceptions import ParseError
from rest_framework.utils import json
from rest_framework.views import APIView

from magsoft_api import CustomAPIException
from magsoft_api.models import Alerts, Users
from magsoft_api.serializers import AlertCreationSerializer
from magsoft_api.views import auth_required, staff_required


class AlertsView(APIView):
    @auth_required
    def delete(self, request):
        if 'id' not in request.query_params:
            raise ParseError(detail="id is a required query parameter.")

        email = request.user.email
        alert_id = request.query_params.get('id')

        count = Alerts.objects.filter(id=alert_id, email=email).delete()

        if count[0] == 0:
            raise CustomAPIException(304, "No alerts were deleted.")
        else:
            return HttpResponse(status=204)

    @staff_required
    def post(self, request):
        data = request.data.copy()

        if 'email' in data:  # If we're given an email
            if isinstance(data['email'], str):  # If it's just one
                email_list = (data['email'],)  # Make the email list have this one item
            else: # Otherwise
                email_list = data['email']  # Set the email list to the list given to us
        else:  # If we aren't given an email
            email_list = Users.objects.values_list('email', flat=True)  # Use all users

        for email in email_list:
            data['email'] = email
            alert = AlertCreationSerializer(data=data)
            if alert.is_valid():
                alert.create(alert.validated_data)
            else:
                return HttpResponse(json.dumps(alert.errors), content_type='application/json', status=400)

        return HttpResponse(status=204)
