from rest_framework import generics

from apps.pages.models import Page, Video, Audio
from .serializers import (
    PageListSerializer,
    PageDetailSerializer
)
from api.pagination import ObjectsListAPIPagination
from apps.pages.tasks import increment_page_content_counter_task

class PageList(generics.ListAPIView):
    queryset = Page.objects.all()
    serializer_class = PageListSerializer
    pagination_class = ObjectsListAPIPagination


class PageDetail(generics.RetrieveAPIView):
    queryset = Page.objects.all()
    serializer_class = PageDetailSerializer

    def get(self, request, *args, **kwargs):
        instance: Page = self.get_object()
        increment_page_content_counter_task.delay(page_id=instance.id)
        return super().get(request, *args, **kwargs)
