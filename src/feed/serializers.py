from rest_framework import serializers

from feed.models import Video


class VideoListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = ("title", "unique_video_id", "description",
                  "published_at", "thumbnail_url", "created_at", "updated_at")


class VideoSearchESSerializer(serializers.Serializer):
    title = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    published_at = serializers.SerializerMethodField()
    thumbnail_url = serializers.SerializerMethodField()
    unique_video_id = serializers.SerializerMethodField()
    created_at = serializers.SerializerMethodField()
    updated_at = serializers.SerializerMethodField()

    class Meta:
        fields = ("title", "description", "published_at",
                  'thumbnail_url', 'unique_video_id', 'created_at', 'updated_at')

    def get_title(self, instance):
        return instance.title

    def get_description(self, instance):
        return instance.description

    def get_published_at(self, instance):
        return instance.published_at

    def get_thumbnail_url(self, instance):
        return instance.thumbnail_url

    def get_unique_video_id(self, instance):
        return instance.unique_video_id

    def get_created_at(self, instance):
        return instance.created_at

    def get_updated_at(self, instance):
        return instance.updated_at