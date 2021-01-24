from elasticsearch_dsl import Q
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.response import Response

from feed.documents import VideoDocument
from feed.models import Video
from feed.pagination import VideoListPagination
from feed.serializers import VideoListSerializer


class VideoListView(ListAPIView):
    queryset = Video.objects.order_by('-published_at').all()
    serializer_class = VideoListSerializer
    pagination_class = VideoListPagination


class VideoSearchView(ListAPIView):
    queryset = Video.objects.all()
    es_queryset = VideoDocument.search()
    serializer_class = VideoListSerializer
    pagination_class = VideoListPagination

    def get_queryset(self):
        return self.es_queryset

    def filter_queryset(self, queryset):
        request = self.request
        q_term = request.query_params.get('q')
        sort_term = request.query_params.get('sort', '-published_at')

        es_queryset = queryset

        if q_term:
            es_query_param = Q("multi_match", query=q_term, fields=["title", "description"])
            es_queryset = es_queryset.query(es_query_param)

        if sort_term:
            sort_params = sort_term
            es_queryset = es_queryset.sort(sort_params)

        return es_queryset

