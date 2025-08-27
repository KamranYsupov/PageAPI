import time
from unittest.mock import patch

from django.urls import reverse
from rest_framework import status
from rest_framework.request import Request
from rest_framework.test import APITestCase, APIClient, APIRequestFactory
from apps.pages.models import Page, Video, Audio
from api.v1.pages.serializers import PageListSerializer, PageDetailSerializer

class PageAPITests(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.factory = APIRequestFactory()
        self.page = Page.objects.create(title="Test Page")
        self.video = Video.objects.create(
            page=self.page,
            title="Test Video",
            video_url="http://example.com/video.mp4"
        )
        self.audio = Audio.objects.create(
            page=self.page,
            title="Test Audio", text="This is a test audio."
        )

    def test_page_list_view(self):
        """Положительный тест для PageListView"""
        request = self.factory.get(
            reverse(
                'api_v1:page-detail',
                kwargs={'pk': self.page.pk}
            )
        )
        response = self.client.get(reverse('api_v1:page-list'))

        serializer_data = PageListSerializer(
            self.page,
            context={'request': Request(request)}
        ).data

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(serializer_data, response.data['results'])

    def test_get_page_details(self):
        """Положительный тест для PageDetailView"""

        response = self.client.get(
            reverse(
                'api_v1:page-detail',
                kwargs={'pk': self.page.pk}
            )
        )
        serializer_data = PageDetailSerializer(self.page).data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(serializer_data, response.data)

    @patch('apps.pages.tasks.increment_page_content_counter_task.delay')
    def test_increment_view_count(self, mock_increment_page_content_counter_task):
        """Тест для проверки вызова increment_page_content_counter_task"""
        response = self.client.get(
            reverse(
                'api_v1:page-detail',
                kwargs={'pk': self.page.pk}
            )
        )
        mock_increment_page_content_counter_task.assert_called_once_with(
            page_id=self.page.pk
        )
