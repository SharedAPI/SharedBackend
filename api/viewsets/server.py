import random
import string

from rest_framework import status, viewsets
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from ..models.server import Server, ServerPlugins
from ..models.plugin import Plugin
from ..serializers.server import ServerSerializer, ServerPluginsSerializer


class ServerViewSet(viewsets.ModelViewSet):
    queryset = Server.objects.all()
    serializer_class = ServerSerializer


class ServerPluginsViewSet(viewsets.ModelViewSet):
    queryset = ServerPlugins.objects.all()
    serializer_class = ServerPluginsSerializer

    def create(self, request, pk=None):
        if request.method != "POST":
            return Response(status=status.HTTP_403_FORBIDDEN)

        serializer = ServerPluginsSerializer(
            data=request.data, context={"request": request}
        )

        if serializer.is_valid():
            server = serializer.data["server"]
            plugin = serializer.data["plugin"]

            try:
                res = ServerPlugins.objects.get(server=server, plugin=plugin)
            except ServerPlugins.DoesNotExist:
                res = None

            if res:
                token = res.token
            else:
                token = "".join(
                    random.choices(string.ascii_letters + string.digits, k=16)
                )
                server = get_object_or_404(Server, pk=server)
                plugin = get_object_or_404(Plugin, pk=plugin)

                obj = ServerPlugins(server=server, plugin=plugin, token=token)
                obj.save()
            return Response({"token": token})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
