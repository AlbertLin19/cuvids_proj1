from django.contrib import admin
from .models import UserCount
from .models import VideoCount

# Register your models here.
admin.site.register(UserCount)
admin.site.register(VideoCount)