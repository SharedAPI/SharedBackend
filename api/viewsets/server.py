from rest_framework import viewsets
from ..models.server import Server, ServerPlugins
from ..serializers.server import ServerSerializer, ServerPluginsSerializer


class ServerViewSet(viewsets.ModelViewSet):
    queryset = Server.objects.all()
    serializer_class = ServerSerializer


class ServerPluginsViewSet(viewsets.ModelViewSet):
    queryset = ServerPlugins.objects.all()
    serializer_class = ServerPluginsSerializer