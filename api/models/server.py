import uuid
from django.db import models
from .plugin import Plugin


class Server(models.Model):

    def __str__(self) -> str:
        return self.name

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    name = models.CharField(max_length=256)

    plugins = models.ManyToManyField(
        Plugin, related_name="servers", through="ServerPlugins"
    )


class ServerPlugins(models.Model):
    server = models.ForeignKey(Server, on_delete=models.RESTRICT)
    plugin = models.ForeignKey(Plugin, on_delete=models.RESTRICT)
    token = models.CharField(max_length=16, null=True, blank=True)