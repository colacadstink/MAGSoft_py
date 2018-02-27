from rest_framework import serializers

from magsoft_api.models import Badges, Settings


class BadgeInfoSerializer(serializers.ModelSerializer):
    badge_this_year = serializers.BooleanField(write_only=True)
    agree = serializers.BooleanField(write_only=True)
    badge_limit_hit = serializers.BooleanField(write_only=True)
    badges_open = serializers.BooleanField(write_only=True)
    badge_cost = serializers.IntegerField(write_only=True)
    payment_due_date = serializers.CharField(write_only=True)

    def to_representation(self, instance):
        ret = super(BadgeInfoSerializer, self).to_representation(instance)
        ret['badge_this_year'] = self.context.get('badge_this_year')
        ret['agree'] = self.context.get('badge_this_year') #TODO: Remove this, it's silly.
        ret['badge_limit_hit'] = Badges.objects.filter(year=Settings['curYear']).count() >= int(Settings['maxBadges'])
        ret['badges_open'] = Settings['badgesOpen']
        ret['badge_cost'] = Settings['badgeCost']
        ret['payment_due_date'] = Settings['paymentDueDate']
        return ret

    class Meta:
        model = Badges
        fields = ('zip', 'extra', 'shirt', 'badge_name', 'badge_data', 'spam', 'badge_added',
                  'badge_this_year', 'agree', 'badge_limit_hit', 'badges_open', 'badge_cost',
                  'payment_due_date')
