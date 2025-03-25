from rest_framework import serializers

from api.models.plugin import Plugin
from api.models.server import Server

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
        server.plugins.add(plugin)
        return {"server": server.id, "plugin": plugin.id}
