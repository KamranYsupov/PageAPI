from django.contrib import admin

from .models import Page, Audio, Video


@admin.register(Page)
class PageAdmin:
    pass

@admin.register(Audio)
class AudioAdmin:
    pass

@admin.register(Video)
class VideoAdmin:
    pass