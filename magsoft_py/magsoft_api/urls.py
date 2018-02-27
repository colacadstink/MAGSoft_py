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
from magsoft_api.views import authentications, registration, alerts, badges

urlpatterns = [
    path('login', authentications.LoginViews.as_view()),
    path('logout', authentications.LogoutViews.as_view()),
    path('whoami', authentications.WhoamiViews.as_view()),

    path('register', registration.RegistrationViews.as_view()),

    path('alerts', alerts.AlertsViews.as_view()),
    path('badges', badges.BadgesViews.as_view()),
]

if(settings.DEBUG):
    def getcsrf(request):
        return HttpResponse(status=204)
    urlpatterns.append(path("getcsrf", getcsrf))
