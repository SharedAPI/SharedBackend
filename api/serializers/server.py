from rest_framework import serializers
from api.models.server import Server


# Serializers define the API representation.
class ServerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Server
        exclude = ["pack"]
