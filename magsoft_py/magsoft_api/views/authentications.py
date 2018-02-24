from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse

from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework.utils import json
from rest_framework.views import APIView

from magsoft_api import CustomAPIException
from magsoft_api.serializers import WhoAmISerializer
from magsoft_api.views import auth_required


class LoginViews(APIView):
    def post(self, request):
        if request.user.is_authenticated:
            raise CustomAPIException(304, "You are already logged in; log out to log in again.")

        try:
            user = authenticate(request, username=request.data['email'], password=request.data['password'])
            if user:
                login(request, user)
                return HttpResponse(status=204)
            else:
                raise AuthenticationFailed()
        except KeyError:
            raise AuthenticationFailed()


class LogoutViews(APIView):
    @auth_required
    def post(self, request):
        logout(request)
        return HttpResponse(status=204)


class WhoamiViews(APIView):
    @auth_required
    def get(self, request):
        whoami = WhoAmISerializer(request.user)
        return Response(whoami.data)
