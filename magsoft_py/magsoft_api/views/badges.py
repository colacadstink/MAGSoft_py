from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.views import APIView

from magsoft_api.models import Badges, Users, Settings
from magsoft_api.serializers.badges import BadgeInfoGetSerializer, BadgeInfoPostSerializer

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

        cereal = BadgeInfoGetSerializer(badge_info, context={'badge_this_year': badge_this_year})
        return Response(cereal.data)

    @auth_required
    def post(self, request):
        data = request.data.copy()

        if request.user.is_staff: # If they're staff, let them manage badges for others
            if 'id' in data and 'email' not in data: # If we've got a UID and not their email
                data['email'] = Users.objects.get(id=data['id']).email # Fetch their email
            elif 'email' not in data: # Otherwise, if we're missing the email
                data['email'] = request.user.email # Use your account's email
            # If we're given an email as a parameter, we'll use that though.
        else: # If they're not staff
            data['email'] = request.user.email # They can only edit their own badge.

        if 'id' in data: # At this point, if there's still an ID,
            del data['id'] # Delete it, because it'll start conflicting with the badge's ID.

        badge = BadgeInfoPostSerializer(data=data)
        if badge.is_valid():
            existing_badge = Badges.objects.filter(email=badge.validated_data['email'], year=badge.validated_data['year'])
            if existing_badge.count() == 1:
                if badge.validated_data['agree']:
                    badge.update(existing_badge.get(), badge.validated_data)
                else:
                    existing_badge.delete()
                    return Response(status=204)
            else:
                badge.create(badge.validated_data)
            return Response(badge.data)
        else:
            return Response(badge.errors, status=400)

    @auth_required
    def delete(self, request):
        data = request.data.copy()

        if request.user.is_staff: # If they're staff, let them manage badges for others
            if 'id' in data and 'email' not in data: # If we've got a UID and not their email
                data['email'] = Users.objects.get(id=data['id']).email # Fetch their email
            elif 'email' not in data: # Otherwise, if we're missing the email
                data['email'] = request.user.email # Use your account's email
            # If we're given an email as a parameter, we'll use that though.
        else: # If they're not staff
            data['email'] = request.user.email # They can only edit their own badge.

        if 'id' in data: # At this point, if there's still an ID,
            del data['id'] # Delete it, because it'll start conflicting with the badge's ID.

        badge = BadgeInfoPostSerializer(data=data)
        if badge.is_valid():
            existing_badge = Badges.objects.filter(email=badge.validated_data['email'], year=badge.validated_data['year'])
            if existing_badge.count() == 1:
                existing_badge.delete()
                return Response(status=204)
            else:
                return Response("No badge exists this year for "+badge.validated_data['email']+".", status=400)
