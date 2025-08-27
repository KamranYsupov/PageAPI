from itertools import chain
from typing import List, Union

from django.db import models
from django.db.models import F, QuerySet
from django.utils.text import gettext_lazy as _

from models.mixins import TimestampModelMixin, UUIDModelMixin


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


class AbstractContent(UUIDModelMixin, TimestampModelMixin):
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
        _('Счетчик просмотров'),
        default=0
    )
    content_type = models.CharField(
        _('Тип контента'),
        max_length=5,
        choices=ContentType.TYPES
    )

    class Meta:
        abstract = True


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

    class Meta:
        verbose_name = _('Видеозапись')
        verbose_name_plural = _('Видеозаписи')

    def __str__(self):
        return f'Видео: {self.title}'


class Audio(AbstractContent):
    """Модель аудио контента"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.content_type = self.ContentType.AUDIO

    text = models.TextField(_('Текст'))

    page = PageForeignKeyField(related_name='audios')


    class Meta:
        verbose_name = _('Аудиозапись')
        verbose_name_plural = _('Аудиозаписи')

    def __str__(self):
        return f'Аудио: {self.title}'


class Page(UUIDModelMixin, TimestampModelMixin):
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


    def __get_content_objects_lists(
            self
    ) -> List[Union[QuerySet[Video], QuerySet[Audio]]]:
        """
        Метод для получения списка query-сетов
        с объектами контента страницы(videos, audios, и т. д.)
        """
        content_objects_lists = [
            self.videos.all(),
            self.audios.all()
        ]

        return content_objects_lists

    def get_content(
            self,
            order_by_reverse_created_at: bool = True
    ) -> List[Union[Video, Audio]]:
        """
        Метод для получения объектов контента статьи
        в виде единого списка
        """

        content_objects_lists = self.__get_content_objects_lists()
        content = chain(*content_objects_lists)

        if order_by_reverse_created_at:
            content = sorted(
                content,
                key=lambda x: x.created_at,
                reverse=True
            )

        return list(content)

    def increment_content_counter(self) -> None:
        """Метод для обновления счетчика просмотров объектов контента статьи"""
        content_objects_lists = self.__get_content_objects_lists()

        for content_list in content_objects_lists:
            content_list.update(counter=F('counter') + 1)
