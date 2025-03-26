from django.db import models

from .plugin import PluginVersion


class DynamicTable(models.Model):
    def __str__(self) -> str:
        return f"{self.plugin_version}_{self.name}"

    name = models.CharField(max_length=256)
    plugin_version = models.ForeignKey(PluginVersion, on_delete=models.CASCADE)
