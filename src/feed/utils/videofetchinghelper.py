from datetime import datetime

import requests
import pyrfc3339
from django.conf import settings
from django.db import IntegrityError
from django.utils import timezone
from django.utils.dateparse import parse_datetime
from rest_framework import status

from feed.utils.modelhelpers.apikeyhelper import APIKeyHelper
from feed.utils.modelhelpers.videohelper import VideoHelper


class APIErrorReason:
    FORBIDDEN = "forbidden"
    QUOTA_EXCEEDED = "quota_exceeded"


class VideoFetchingHelper:
    def __init__(self, query_term):
        self.query_term = query_term

        self.api_key_helper = APIKeyHelper()
        self.video_helper = VideoHelper()

        self._api_key = None

    def invalidate_current_key(self):
        self._api_key = None

    def threshold_reached_for_api_key(self):
        current_key = self._api_key
        self.invalidate_current_key()
        self.api_key_helper.mark_threshold_reached(current_key)

    def get_published_after(self, default: datetime = None):
        """Fetches the time of latest video that was published that is stored in DB.
            If DB is empty, then `default` param is returned. If 'default' param is not specified,
                then timezone.now() time is returned.
        Args:
            default (datetime) : Optional. Default datetime that should be returned if DB is empty

        Returns:
            datetime
        """
        get_latest_instance_order_by_published_at = (
            self.video_helper.get_latest_instance_order_by_published_at()
        )
        if get_latest_instance_order_by_published_at:
            return get_latest_instance_order_by_published_at.published_at

        if default:
            return default

        return timezone.now()

    def get_key(self):
        if self._api_key is None:
            self._api_key = self.api_key_helper.get_key()
        return self._api_key

    def get_url(self):
        return settings.YOUTUBE_API["url"]

    def fetch_videos(self, max_results=10):
        query = self.query_term
        api_key = self.get_key()
        url = self.get_url()

        published_after = self.get_published_after()
        published_after_rfc3339_format = pyrfc3339.generate(published_after)

        params = {
            "part": "snippet",
            "maxResults": max_results,
            "q": query,
            "key": api_key,
            "publishedAfter": published_after_rfc3339_format,
            "type": "video",
        }
        print(params)
        response = requests.get(url, params=params)
        print(f"Response from youtube api with status: {response.status_code}")
        return response

    def on_403_status_code(self, response):
        try:
            reason = response["error"]["errors"][-1]["reason"]
            if reason == APIErrorReason.QUOTA_EXCEEDED:
                self.threshold_reached_for_api_key()

        except (KeyError, IndexError):
            pass

    def on_200_status_code(self, response):
        data = response.json()

        video_info_list = data.get("items")
        if video_info_list is None:
            return

        for video_info in video_info_list:
            snippet_info = video_info.get("snippet")
            if snippet_info is None:
                continue

            published_at = parse_datetime(snippet_info["publishedAt"])

            data = {
                "title": snippet_info.get("title", ""),
                "unique_video_id": video_info.get("id", {}).get("videoId"),
                "description": snippet_info.get("description", ""),
                "thumbnail_url": snippet_info.get("thumbnails", {})
                .get("default", {})
                .get("url", ""),
                "published_at": published_at,
                "extras": video_info,
            }
            try:
                self.video_helper.create_instance(**data)
            except IntegrityError:
                print(
                    f"Video with {video_info.get('id', {}).get('videoId')} was already added"
                )

    def handle_response(self, response):
        if response.status_code == status.HTTP_403_FORBIDDEN:
            self.on_403_status_code(response=response)
        if response.status_code == status.HTTP_200_OK:
            self.on_200_status_code(response=response)
        else:
            pass

    def run(self):
        response = self.fetch_videos()
        self.handle_response(response=response)
