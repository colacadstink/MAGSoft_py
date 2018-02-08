"""magsoft_py URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.http import HttpResponse
from django.urls import path

import settings
from magsoft_api.views import authentications, registration

urlpatterns = [
    path('login', authentications.AuthenticationViews.login),
    path('logout', authentications.AuthenticationViews.logout),
    path('whoami', authentications.AuthenticationViews.whoami),
    path('register', registration.RegistrationViews.register),
]

if(settings.DEBUG):
    def getcsrf(request):
        return HttpResponse()
    urlpatterns.append(path("getcsrf", getcsrf))
