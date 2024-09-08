from rest_framework import serializers
from ..models.plugin import Plugin

class PluginSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plugin
        fields = ['id', 'name', 'schema']

    # def create(self, validated_data):
    #     # TODO: creation all table in schema
    #     return super().create(validated_data)
    
    # def update(self, instance, validated_data):
    #     # TODO: update all table in schema
    #     return super().update(instance, validated_data)