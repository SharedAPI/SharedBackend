from datetime import timedelta
import secrets
from django.db import models
from django.utils import timezone

from api.models.plugin import PluginVersion


class Pack(models.Model):
    def __str__(self) -> str:
        return f"{self.server}_pack"  # type: ignore

    plugin_versions = models.ManyToManyField(
        PluginVersion, related_name="packs", through="PackAndPlugins"
    )
    # It's the first date of a plugin subscription,
    billing_date = models.DateField()


class PackAndPlugins(models.Model):
    pack = models.ForeignKey(Pack, on_delete=models.RESTRICT)
    plugin_version = models.ForeignKey(PluginVersion, on_delete=models.RESTRICT)
    token = models.CharField(max_length=16, null=True, blank=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    def save(self, *args, **kwargs):
        if not self.token:
            self.token = secrets.token_hex(8)
        if not self.end_date:
            self.end_date = timezone.now() + timedelta(30)
        super().save(*args, **kwargs)

    def refresh_token(self):
        # TODO Get billing information and check if is on date
        if True:
            self.end_date += timedelta(30)
            self.save()

    def is_token_expired(self):
        return timezone.now() > self.end_date
