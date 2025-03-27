import uuid

from django.db import models
from api.models.pack import Pack


class Server(models.Model):
    def __str__(self) -> str:
        return f"{self.name}_[{self.id}]"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=256)

    pack = models.OneToOneField(Pack, on_delete=models.CASCADE, null=True, blank=True)
