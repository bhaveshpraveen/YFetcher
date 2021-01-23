from feed.models import Video


class VideoHelper:
    model = Video

    def get_latest_instance_order_by_published_at(self):
        return self.model.objects.order_by("-published_at").first()

    def create_instance(self, *args, **kwargs):
        print(f"Creating {self.model.__class__.__name__} instance with data: {kwargs}")
        instance = self.model.objects.create(*args, **kwargs)
        print(f"Created {self.model.__class__.__name__} instance")
        return instance
