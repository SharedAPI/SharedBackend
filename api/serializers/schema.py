from rest_framework import serializers


class SchemaSerializer(serializers.Serializer):
    schema = serializers.JSONField()
