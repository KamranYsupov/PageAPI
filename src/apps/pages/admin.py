from django.contrib import admin

from .models import Page, Audio, Video


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    pass

@admin.register(Audio)
class AudioAdmin(admin.ModelAdmin):
    pass

@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    pass