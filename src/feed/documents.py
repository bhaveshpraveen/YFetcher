from django_elasticsearch_dsl import Document
from django_elasticsearch_dsl.registries import registry

from feed.models import Video


@registry.register_document
class VideoDocument(Document):
    class Index:
        name = 'videos'
        settings = {'number_of_shards': 1,
                    'number_of_replicas': 0}

    class Django:
        model = Video

        fields = [
            'title',
            'description',
            'published_at',
            'unique_video_id',
            'thumbnail_url'
        ]
