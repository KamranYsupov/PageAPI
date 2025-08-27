import time
import uuid
from typing import Union

import loguru
from django.core.cache import cache
from django.conf import settings
from django.db import transaction

from config.celery import app
from apps.pages.models import Page

@app.task()
def increment_page_content_counter_task(
        page_id: Union[uuid.UUID, str],
) -> None:
    """
    Задача для атомарного обновления счетчика просмотров
    объектов контента статьи
    """

    with transaction.atomic():
        page = Page.objects.get(id=page_id)
        page.increment_content_counter()
