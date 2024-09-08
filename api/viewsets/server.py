from rest_framework import viewsets
from ..models.server import Server
from ..serializers.server import ServerSerializer


class ServerViewSet(viewsets.ModelViewSet):
    queryset = Server.objects.all()
    serializer_class = ServerSerializer