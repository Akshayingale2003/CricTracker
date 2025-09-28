from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Profile)
admin.site.register(Team)
admin.site.register(Player)
admin.site.register(BattingPerformance)
admin.site.register(BallingPerformance)
admin.site.register(WicketKeeperPerformance)
admin.site.register(FieldingPerformance)