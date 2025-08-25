from django.db import models
from django.utils.text import gettext_lazy as _


class TimestampMixin:
    created_at = models.DateTimeField(
        _('Дата создания'),
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        _('Дата последнего обновления'),
        auto_now=True
    )
