from typing import List

from django.db import models
from django.db.models import F
from django.utils.text import gettext_lazy as _

from models.mixins import TimestampMixin


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

    title = models.CharField(
        _('Название'),
        max_length=200
    )
    counter = models.PositiveIntegerField(
        _('Счетчик просмотров'),
        default=0
    )

    class Meta:
        abstract = True


class Video(AbstractContent):
    """Модель видео контента"""

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
    text = models.TextField(_('Текст'))

    page = PageForeignKeyField(related_name='audios')

    def __str__(self):
        return f'Аудио: {self.title}'


class Page(models.Model, TimestampMixin):
    """Модель страницы"""

    title = models.CharField(
        _('Название'),
        max_length=200
    )

    def __str__(self):
        return self.title

    def get_content(self) -> List[Video | Audio]:
        content = []
        content.extend(self.videos.all())
        content.extend(self.audios.all())

        return content

    def increment_content_counter(self):
        self.videos.all().update(counter=F('counter') + 1)
        self.audios.all().update(counter=F('counter') + 1)
