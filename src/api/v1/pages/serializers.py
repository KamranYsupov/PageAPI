from itertools import chain

from rest_framework import serializers
from apps.pages.models import Page, Video, Audio


class BaseContentSerializer(serializers.ModelSerializer):

    class Meta:
        exclude = ('page', )


class VideoSerializer(BaseContentSerializer):
    class Meta(BaseContentSerializer.Meta):
        model = Video


class AudioSerializer(BaseContentSerializer):
    class Meta(BaseContentSerializer.Meta):
        model = Audio


class BasePageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Page
        fields = (
            'id',
            'title',
        )


class PageListSerializer(BasePageSerializer):
    detail_url = serializers.HyperlinkedIdentityField(
        view_name='api_v1:page-detail',
        lookup_field='pk',
    )

    class Meta(BasePageSerializer.Meta):
        fields = BasePageSerializer.Meta.fields + ('detail_url', )


class PageDetailSerializer(BasePageSerializer):
    content = serializers.SerializerMethodField()

    class Meta(BasePageSerializer.Meta):
        fields = BasePageSerializer.Meta.fields + ('content', )

    def get_content(self, obj):
        videos = VideoSerializer(obj.videos.all(), many=True).data
        audios = AudioSerializer(obj.audios.all(), many=True).data

        content = chain(videos, audios,)
        sorted_content = sorted(content, key=lambda x: x['page_position'])

        return list(sorted_content)