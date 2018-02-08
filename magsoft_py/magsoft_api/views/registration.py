from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.utils import json

from magsoft_api.serializers import UserSerializer


class RegistrationViews:
    @api_view(['POST'])
    def register(request):
        data = json.loads(request.body)
        #TODO: Remove double passwords from the form

        #Encrypt the password
        if "password" in data:

            pass

        user = UserSerializer(data=data)
        if user.is_valid():
            user.create(user.validated_data)
            return HttpResponse(status=204)
        else:
            return HttpResponse(json.dumps(user.errors), status=400)
