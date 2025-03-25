from django.db import models

from .table import DynamicTable


class DynamicColumn(models.Model):
    def __str__(self) -> str:
        return f"{self.table.plugin.name}_{self.table.name}_{self.name}"

    table = models.ForeignKey(DynamicTable, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=50)
    is_primary = models.BooleanField(default=False)
