from django.db.models import F
from rest_framework import generics
from apps.pages.models import Page, Video, Audio
from .serializers import (
    PageListSerializer,
    PageDetailSerializer
)


class PageList(generics.ListAPIView):
    queryset = Page.objects.all()
    serializer_class = PageListSerializer


class PageDetail(generics.RetrieveAPIView):
    queryset = Page.objects.all()
    serializer_class = PageDetailSerializer

    def get(self, request, *args, **kwargs):
        instance: Page = self.get_object()
        instance.increment_content_counter()
        return super().get(request, *args, **kwargs)
