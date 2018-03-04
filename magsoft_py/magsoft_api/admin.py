from django.contrib import admin

# Register your models here.
from magsoft_api.models import Users, Canroompreauth, Settings, BadgeExtras

admin.site.register(BadgeExtras)
admin.site.register(Canroompreauth)
admin.site.register(Settings)
admin.site.register(Users)
