from rest_framework.response import Response
from rest_framework.views import APIView

from magsoft_api.models import Badges, Users, Settings
from magsoft_api.serializers.badges import BadgeInfoSerializer

from magsoft_api.views import auth_required


class BadgesViews(APIView):
    @auth_required
    def get(self, request):
        email = request.user.email
        if 'id' in request.query_params and request.user.is_staff:
            user_id = request.query_params['id']
            email = Users.objects.get(id=user_id).email

        my_badges = Badges.objects.filter(email=email)
        badge_info = my_badges.filter(year=int(Settings['curYear']))
        if badge_info.count() == 1:
            badge_info = badge_info.get()
            badge_this_year = True
        else:
            badge_this_year = False
            badge_info = my_badges.filter(year=int(Settings['curYear'])-1)
            if badge_info.count() == 1:
                badge_info = badge_info.get()
            else:
                badge_info = None

        cereal = BadgeInfoSerializer(badge_info, context={'badge_this_year': badge_this_year})
        return Response(cereal.data)

    @auth_required
    def put(self, request):
        pass

    @auth_required
    def delete(self, request):
        pass
