from rest_framework import serializers
from ..models.server import Server, ServerPlugins

class ServerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Server
        fields = ['id', 'name', 'plugins']


class ServerPluginsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServerPlugins
        fields = ['id', 'server', 'plugin', 'token']
        depth = 0