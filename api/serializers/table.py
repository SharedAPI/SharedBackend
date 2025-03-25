from rest_framework import serializers

from api.models.plugin import Plugin
from api.models.table import DynamicTable

# Serializers define the API representation.


class DynamicTableSerializer(serializers.ModelSerializer):
    plugin = serializers.PrimaryKeyRelatedField(queryset=Plugin.objects.all())

    class Meta:
        model = DynamicTable
        fields = "__all__"
        depth = 1
