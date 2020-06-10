from django.contrib import admin
from .models import UserCount, VideoCount, WatchData

# Register your models here.
admin.site.register(UserCount)
admin.site.register(VideoCount)
admin.site.register(WatchData)