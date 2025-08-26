from django.contrib import admin

from .models import Page, Audio, Video


class AbstractContentInline(admin.TabularInline):
    """Абстрактный класс inline поля контента"""
    extra = 1
    exclude = ('content_type', 'counter',)

    class Meta:
        abstract = True

class AudioInline(AbstractContentInline):
    model = Audio

class VideoInline(AbstractContentInline):
    model = Video


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    inlines = [
        VideoInline,
        AudioInline,
    ]


class AbstractContentAdmin(admin.ModelAdmin):
    """Абстрактный класс для админ-панели контента"""
    exclude = ('content_type', 'counter',)

    class Meta:
        abstract = True

@admin.register(Audio)
class AudioAdmin(AbstractContentAdmin):
    pass

@admin.register(Video)
class VideoAdmin(AbstractContentAdmin):
    pass