from rest_framework.views import APIView

from magsoft_api.models import Badges, Users

from magsoft_api.views import auth_required


class BadgesViews(APIView):
    @auth_required
    def get(self, request):
        email = request.user.email
        if 'id' in request.query_params and request.user.is_staff:
            user_id = request.query_params['id']
            email = Users.objects.get(id=user_id).email

        myBadges = Badges.objects.filter(email=email)
        #try and filter this year
        #if fail get last year
        #if fail get blank

    @auth_required
    def put(self, request):
        pass

    @auth_required
    def delete(self, request):
        pass