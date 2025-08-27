from typing import Union, Dict, List

import loguru
from django import forms
from django.contrib import admin, messages

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
    search_fields = 'title__istartswith',
    inlines = [
        VideoInline,
        AudioInline,
    ]
