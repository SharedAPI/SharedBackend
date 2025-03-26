from rest_framework import serializers
from api.models.plugin import Plugin, PluginVersion
from django.utils import timezone


from api.models.server import ServerPluginsVersion


# Serializers define the API representation.
class PluginSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plugin
        fields = "__all__"


class PluginVersionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PluginVersion
        fields = "__all__"


class ReadOnlyPluginVersionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PluginVersion
        exclude = ["schema", "plugin"]


class DeprecatedPluginVersionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PluginVersion
        fields = ["deprecated"]


class AddPluginVersionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PluginVersion
        exclude = ["plugin"]

    def create(self, validated_data):
        plugin = self.context["plugin"]
        version = validated_data["version"]
        schema = validated_data["schema"]

        plugin_version, _ = PluginVersion.objects.get_or_create(
            plugin=plugin, version=version, schema=schema
        )
        return plugin_version


class AddPluginSerializer(serializers.Serializer):
    plugin_version = serializers.PrimaryKeyRelatedField(queryset=PluginVersion.objects.all())
    start_date = serializers.DateTimeField(default=timezone.now())

    def create(self, validated_data):
        server = self.context["server"]
        plugin_version = validated_data["plugin_version"]
        start_date = validated_data["start_date"]
        server_plugin, _ = ServerPluginsVersion.objects.get_or_create(
            server=server, plugin_version=plugin_version, start_date=start_date
        )

        return server_plugin
