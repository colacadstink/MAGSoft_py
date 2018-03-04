from rest_framework import serializers

from magsoft_api.models import Badges, Settings, BadgeExtras, Users


class BadgeExtrasSerializer(serializers.ModelSerializer):
    class Meta:
        model = BadgeExtras
        fields = ('text', 'cost', 'has_shirt', 'has_name')


class BadgeInfoGetSerializer(serializers.ModelSerializer):
    badge_this_year = serializers.BooleanField(write_only=True)
    agree = serializers.BooleanField(write_only=True)
    badge_limit_hit = serializers.BooleanField(write_only=True)
    badges_open = serializers.BooleanField(write_only=True)
    badge_cost = serializers.IntegerField(write_only=True)
    payment_due_date = serializers.CharField(write_only=True)
    extras = serializers.JSONField(write_only=True)

    def to_representation(self, instance):
        ret = super(BadgeInfoGetSerializer, self).to_representation(instance)
        ret['badge_this_year'] = self.context.get('badge_this_year')
        ret['agree'] = self.context.get('badge_this_year') #TODO: Remove this, it's silly.
        ret['badge_limit_hit'] = Badges.objects.filter(year=Settings['curYear']).count() >= int(Settings['maxBadges'])
        ret['badges_open'] = Settings['badgesOpen']
        ret['badge_cost'] = Settings['badgeCost']
        ret['payment_due_date'] = Settings['paymentDueDate']
        ret['extras'] = BadgeExtrasSerializer(BadgeExtras.objects.all(), many=True).data
        return ret

    class Meta:
        model = Badges
        fields = ('zip', 'extra', 'shirt', 'badge_name', 'badge_data', 'spam', 'badge_added', 'badge_this_year',
                  'agree', 'badge_limit_hit', 'badges_open', 'badge_cost', 'payment_due_date', 'extras')


class BadgeInfoPostSerializer(serializers.ModelSerializer):
    agree = serializers.BooleanField(write_only=True)
    extra = serializers.IntegerField(required=False, default=0)
    shirt = serializers.IntegerField(required=False)
    badge_name = serializers.CharField(required=False)
    year = serializers.IntegerField(required=False, default=lambda: Settings['curYear'])

    def validate(self, attrs):
        # The level you're at is the largest value that's less than or equal to your contribution.
        extra_level = BadgeExtras.objects.filter(cost__lte=attrs['extra']).order_by('cost').last()

        if extra_level.has_shirt:
            if 'shirt' not in attrs:
                raise serializers.ValidationError("At this contribution level, shirt size is required.")
        else:
            attrs['shirt'] = 0

        if extra_level.has_name:
            if 'badge_name' not in attrs:
                attrs['badge_name'] = attrs['email'].first_name+" "+attrs['email'].last_name
        else:
            attrs['badge_name'] = ''

        return attrs

    class Meta:
        model = Badges
        fields = ('email', 'zip', 'extra', 'shirt', 'badge_name', 'spam', 'agree', 'year')
        validators = []
