from itertools import chain
from typing import List

from django.db import models
from django.db.models import F
from django.utils.text import gettext_lazy as _

from models.mixins import TimestampModelMixin


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


class AbstractContent(models.Model):
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


class Video(AbstractContent, TimestampModelMixin):
    """Модель видео контента"""

    video_url = models.URLField(_('URL видео'))
    subtitles_url = models.URLField(
        _('URL субтитров'),
        blank=True,
        null=True,
        default=None
    )

    page = PageForeignKeyField(related_name='videos')

    class Meta:
        verbose_name = _('Видеозапись')
        verbose_name_plural = _('Видеозаписи')

    def __str__(self):
        return f'Видео: {self.title}'


class Audio(AbstractContent, TimestampModelMixin):
    """Модель аудио контента"""
    text = models.TextField(_('Текст'))

    page = PageForeignKeyField(related_name='audios')


    class Meta:
        verbose_name = _('Аудиозапись')
        verbose_name_plural = _('Аудиозаписи')

    def __str__(self):
        return f'Аудио: {self.title}'


class Page(TimestampModelMixin):
    """Модель страницы"""

    title = models.CharField(
        _('Название'),
        max_length=200
    )

    class Meta:
        verbose_name = _('Страница')
        verbose_name_plural = _('Страницы')

    def __str__(self):
        return self.title

    def get_content(
            self,
            order_by_reverse_created_at: bool = True
    ) -> List[Video | Audio]:
        content = chain(
            self.videos.all(),
            self.audios.all()
        )

        if order_by_reverse_created_at:
            content = sorted(
                content,
                key=lambda x: x.created_at,
                reverse=True
            )

        return list(content)

    def increment_content_counter(self):
        self.videos.all().update(counter=F('counter') + 1)
        self.audios.all().update(counter=F('counter') + 1)
