from rest_framework.pagination import LimitOffsetPagination


class VideoListPagination(LimitOffsetPagination):
    default_limit = 10
    max_limit = 30


class VideoSearchESPagination(LimitOffsetPagination):
    default_limit = 10
    max_limit = 30
