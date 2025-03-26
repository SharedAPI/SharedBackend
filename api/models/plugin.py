import uuid
from django.db import models


class Plugin(models.Model):
    def __str__(self) -> str:
        return self.name

    name = models.CharField(max_length=256)
    description = models.CharField(max_length=4096)


class PluginVersion(models.Model):
    def __str__(self) -> str:
        return f"{self.plugin.name}_{self.version}"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    version = models.CharField(max_length=32)
    plugin = models.ForeignKey(Plugin, on_delete=models.RESTRICT)
    # In schema will be stored the database schema that has to be created
    schema = models.JSONField(null=True, blank=True)
