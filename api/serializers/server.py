from rest_framework import serializers
from ..models.server import Server

class ServerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Server
        fields = ['id', 'name']