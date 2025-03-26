from rest_framework import serializers
from django.utils import timezone

from api.models.plugin import Plugin
from api.models.server import Server, ServerPlugins


# Serializers define the API representation.
class ServerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Server
        exclude = ["plugins"]


class AddPluginSerializer(serializers.Serializer):
    plugin = serializers.PrimaryKeyRelatedField(queryset=Plugin.objects.all())
    start_date = serializers.DateTimeField(default=timezone.now())

    def create(self, validated_data):
        server = self.context["server"]
        plugin = validated_data["plugin"]
        start_date = validated_data["start_date"]
        server_plugin, _ = ServerPlugins.objects.get_or_create(
            server=server, plugin=plugin, start_date=start_date
        )

        return server_plugin
