from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.utils import json
from rest_framework.views import APIView

from magsoft_api.serializers import UserSerializer


class RegistrationViews(APIView):
    def post(self, request):
        #TODO: Remove double passwords from the form

        user = UserSerializer(data=request.data)
        if user.is_valid():
            user.create(user.validated_data)
            return HttpResponse(status=204)
        else:
            return HttpResponse(json.dumps(user.errors), content_type='application/json', status=400)
