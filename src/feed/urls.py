from django.urls import path

from feed.views import VideoListView, VideoSearchView

urlpatterns = [
    path("list/", VideoListView.as_view()),
    path("search/", VideoSearchView.as_view()),
]
