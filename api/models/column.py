from django.db import models

from .table import DynamicTable


class DynamicColumn(models.Model):
    def __str__(self) -> str:
        return f"{self.table}_{self.name}"

    table = models.ForeignKey(DynamicTable, on_delete=models.CASCADE)
    name = models.CharField(max_length=256)
    type = models.CharField(max_length=256)
    is_primary = models.BooleanField(default=False)
