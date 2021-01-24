from django.db import models
from django.utils.translation import ugettext_lazy as _


class Video(models.Model):
    title = models.CharField(_("Title"), max_length=128, db_index=True)
    unique_video_id = models.CharField(_("ETag"), max_length=128, db_index=True)
    description = models.TextField(_("Description"))
    published_at = models.DateTimeField(
        _("Video Published At"), db_index=True, null=True
    )
    thumbnail_url = models.TextField(_("Thumbnail URL"), blank=True, default="")

    created_at = models.DateTimeField(_("Created At"), auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(_("Updated At"), auto_now=True, db_index=True)

    extras = models.JSONField(null=True)

    def __str__(self):
        return f"{self.title}: {self.thumbnail_url}"


class APIKey(models.Model):
    api_secret = models.CharField(
        _("API Key"), max_length=128, unique=True, db_index=True
    )
    threshold_reached = models.BooleanField(_("Threshold Reached"), default=False)
    threshold_reached_on = models.DateField(_("Threshold Reached on Date"), null=True)

    created_at = models.DateTimeField(_("Created At"), auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(_("Updated At"), auto_now=True, db_index=True)

    extras = models.JSONField(null=True)

    def __str__(self):
        return f"{self.api_secret}: {self.threshold_reached}"
