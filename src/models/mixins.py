import uuid

from django.db import models
from django.utils.text import gettext_lazy as _


class TimestampModelMixin(models.Model):
    created_at = models.DateTimeField(
        _('Дата создания'),
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        _('Дата последнего обновления'),
        auto_now=True
    )

    class Meta:
        abstract = True
        ordering = ['-created_at']


class UUIDModelMixin(models.Model):
    id = models.UUIDField(
        default=uuid.uuid4,
        primary_key=True,
        unique=True,
        editable=False,
        db_index=True
    )

    class Meta:
        abstract = True

