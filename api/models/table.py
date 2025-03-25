from django.db import models

from .plugin import Plugin


class DynamicTable(models.Model):
    def __str__(self) -> str:
        return f"{self.plugin.name}_{self.name}"

    name = models.CharField(max_length=256)
    plugin = models.ForeignKey(Plugin, on_delete=models.CASCADE)
