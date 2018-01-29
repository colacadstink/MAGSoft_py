from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.decorators import api_view

from rest_framework.response import Response
from rest_framework.utils import json

from magsoft_api.serializers import WhoAmISerializer


def auth_required(func):
    def wrapper(request):
        if request.user.is_authenticated:
            return func(request)
        else:
            return HttpResponse(status=401)
    return wrapper

class AuthenticationViews:
    @api_view(['POST'])
    def login(request):
        data = json.loads(request.body)
        try:
            user = authenticate(request, username=data['email'], password=data['password'])
            if user:
                login(request, user)
                return HttpResponse(status=204)
            else:
                return HttpResponse(status=401)
        except KeyError:
            return HttpResponse(status=400)

    @api_view(['POST'])
    @auth_required
    def logout(request):
        logout(request)
        return HttpResponse(status=204)


    @api_view(['GET'])
    @auth_required
    def whoami(request):
        whoami = WhoAmISerializer(request.user)
        return Response(whoami.data)


