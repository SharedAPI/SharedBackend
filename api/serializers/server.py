from rest_framework import serializers

from api.models.plugin import Plugin
from api.models.server import Server
from api.serializers.plugin import PluginSerializer

# Serializers define the API representation.


class ServerSerializer(serializers.ModelSerializer):
    plugins = PluginSerializer(many=True, read_only=True)

    class Meta:
        model = Server
        fields = "__all__"


class ServerPluginSerializer(serializers.Serializer):
    plugin = serializers.PrimaryKeyRelatedField(queryset=Plugin.objects.all())

    def create(self, validated_data):
        server = self.context["server"]
        plugin = validated_data["plugin"]
        server.plugins.add(plugin)
        return {"server": server.id, "plugin": plugin.id}
