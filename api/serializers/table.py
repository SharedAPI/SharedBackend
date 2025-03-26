from rest_framework import serializers

from api.models.plugin import PluginVersion
from api.models.table import DynamicTable

# Serializers define the API representation.


class DynamicTableSerializer(serializers.ModelSerializer):
    plugin_version = serializers.PrimaryKeyRelatedField(
        queryset=PluginVersion.objects.all()
    )

    class Meta:
        model = DynamicTable
        fields = "__all__"
        depth = 1
