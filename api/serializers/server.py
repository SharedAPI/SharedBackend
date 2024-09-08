from rest_framework import serializers
from ..models.server import Server, ServerPlugins

class ServerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Server
        fields = ['id', 'name', 'plugins']


class ServerPluginsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ServerPlugins
        fields = ['id', 'server', 'plugin', 'token']

    def create(self, validated_data):
        # TODO: verify if link exist and return token or create and return
        return super().create(validated_data)