from typing import Any

from django.db import models
from django.utils.text import gettext_lazy as _

from models.mixins import TimestampMixin


class Page(models.Model, TimestampMixin):
    """Модель страницы"""

    title = models.CharField(
        _('Название'),
        max_length=200
    )

    def __str__(self):
        return self.title


class PageForeignKeyField(models.ForeignKey):
    """ForeignKey поле к модели Page"""
    def __init__(
            self,
            *,
            related_name,
            on_delete = models.CASCADE,
            **kwargs
    ):
        super().__init__(
            to='pages.Page',
            on_delete=on_delete,
            related_name=related_name,
    )


class AbstractContent(models.Model, TimestampMixin):
    """Абстрактная модель контента"""

    class ContentType:
        VIDEO = 'VIDEO'
        AUDIO = 'AUDIO'

        TYPES = (
            (VIDEO, _('Видео')),
            (AUDIO, _('Аудио')),
        )

    title = models.CharField(
        _('Название'),
        max_length=200
    )
    counter = models.PositiveIntegerField(
        _('Счетчик'),
        default=0
    )
    content_type = models.CharField(
        _('Тип контента'),
        max_length=5,
        choices=ContentType.TYPES
    )

    class Meta:
        abstract = True

    def increment_counter(self):
        self.counter += 1
        self.save()


class Video(AbstractContent):
    """Модель видео контента"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.content_type = self.ContentType.VIDEO

    video_url = models.URLField(_('URL видео'))
    subtitles_url = models.URLField(
        _('URL субтитров'),
        blank=True,
        null=True,
        default=None
    )

    page = PageForeignKeyField(related_name='videos')

    def __str__(self):
        return f'Видео: {self.title}'


class Audio(AbstractContent):
    """Модель аудио контента"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.content_type = self.ContentType.AUDIO

    text = models.TextField(_('Текст'))

    page = PageForeignKeyField(related_name='audios')

    def __str__(self):
        return f'Аудио: {self.title}'

