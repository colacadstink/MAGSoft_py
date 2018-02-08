from django.http import HttpResponse


def auth_required(func):
    def wrapper(request):
        if request.user.is_authenticated:
            return func(request)
        else:
            return HttpResponse(status=401)
    return wrapper
