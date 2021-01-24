from django.conf import settings
from django.db import IntegrityError
from django.db.models import Q
from django.utils import timezone

from feed.models import APIKey


class APIKeyHelper:
    model = APIKey

    def mark_threshold_reached(self, key):
        try:
            instance = self.model.objects.get(api_secret=key)
            instance.threshold_reached = True
            instance.threshold_reached_on = timezone.now().date()
            instance.save()
        except self.model.DoesNotExist:
            pass

    def get_key(self):
        date_today = timezone.now().date()
        api_key_instance = self.model.objects.filter(
            Q(threshold_reached=False)
            | Q(threshold_reached=True, threshold_reached_on__lt=date_today)
        ).first()

        if not api_key_instance:
            raise Exception("All keys exhaused")

        return api_key_instance.api_secret

    @classmethod
    def add_keys(cls):
        api_keys = settings.YOUTUBE_API["api_keys"]

        for api_key in api_keys:
            try:
                cls.model.objects.create(
                    api_secret=api_key,
                    threshold_reached=False,
                )
            except IntegrityError:
                pass
        print(f"Added youtube api keys")
