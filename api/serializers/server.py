from rest_framework import serializers

from api.models.plugin import Plugin
from api.models.server import Server, ServerPlugins


# Serializers define the API representation.
class ServerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Server
        exclude = ["plugins"]


class AddPluginSerializer(serializers.Serializer):
    plugin = serializers.PrimaryKeyRelatedField(queryset=Plugin.objects.all())

    def create(self, validated_data):
        server = self.context["server"]
        plugin = validated_data["plugin"]
        server_plugin, _ = ServerPlugins.objects.get_or_create(
            server=server, plugin=plugin
        )

        return {"server": server_plugin.server, "plugin": server_plugin.plugin}
