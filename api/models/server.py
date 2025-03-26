import uuid
import secrets

from django.db import models
from django.utils import timezone

from datetime import timedelta
from .plugin import PluginVersion


class Server(models.Model):
    def __str__(self) -> str:
        return f"{self.name}_[{self.id}]"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    name = models.CharField(max_length=256)

    plugin_versions = models.ManyToManyField(
        PluginVersion, related_name="servers", through="ServerPluginsVersion"
    )


class ServerPluginsVersion(models.Model):
    server = models.ForeignKey(Server, on_delete=models.RESTRICT)
    plugin_version = models.ForeignKey(PluginVersion, on_delete=models.RESTRICT)
    token = models.CharField(max_length=16, null=True, blank=True)
    start_date = models.DateTimeField()
    expire_date = models.DateTimeField()

    def save(self, *args, **kwargs):
        if not self.token:
            self.token = secrets.token_hex(8)
        if not self.expire_date:
            self.expire_date = timezone.now() + timedelta(30)
        super().save(*args, **kwargs)

    def refresh_token(self):
        # TODO Get billing information and check if is on date
        if True:
            self.expire_date += timedelta(30)
            self.save()

    def is_token_expired(self):
        return timezone.now() > self.expire_date
