from rest_framework import serializers

from api.models.plugin import Plugin


# Serializers define the API representation.


class PluginSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plugin
        fields = "__all__"


class ReadOnlyPluginSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plugin
        exclude = ["schema"]
