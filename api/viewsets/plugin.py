from rest_framework import viewsets
from ..models.plugin import Plugin
from ..serializers.plugin import PluginSerializer


class PluginViewSet(viewsets.ModelViewSet):
    queryset = Plugin.objects.all()
    serializer_class = PluginSerializer