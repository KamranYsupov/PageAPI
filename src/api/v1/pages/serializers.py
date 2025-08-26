from itertools import chain

from rest_framework import serializers
from apps.pages.models import Page, Video, Audio


class ContentSerializerMetaMixin:
    exclude = ('page',)


class VideoSerializer(serializers.ModelSerializer):
    class Meta(ContentSerializerMetaMixin):
        model = Video


class AudioSerializer(serializers.ModelSerializer):
    class Meta(ContentSerializerMetaMixin):
        model = Audio


class BasePageSerializerMeta:
    model = Page
    fields = (
        'id',
        'title',
    )


class PageListSerializer(serializers.ModelSerializer):
    detail_url = serializers.HyperlinkedIdentityField(
        view_name='api:page-detail',
        lookup_field='pk',
    )

    class Meta(BasePageSerializerMeta):
        fields = BasePageSerializerMeta.fields + ('detail_url', )


class PageDetailSerializer(serializers.ModelSerializer):
    content = serializers.SerializerMethodField()

    class Meta(BasePageSerializerMeta):
        fields = BasePageSerializerMeta.fields + ('content', )

    def get_content(self, obj):
        videos = VideoSerializer(obj.videos.all(), many=True).data
        audios = AudioSerializer(obj.audios.all(), many=True).data

        content = chain(
            videos,
            audios,
        )

        sorted_content = sorted(content, key=lambda x: x['created_at'])

        return list(sorted_content)