from http import HTTPMethod

from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.decorators import action

from api.models.server import Server
from api.serializers.server import ServerPluginSerializer, ServerSerializer
from api.utils import CustomResponseHandler


class ServerViewSet(viewsets.ModelViewSet, CustomResponseHandler):
    queryset = Server.objects.all()
    serializer_class = ServerSerializer
    # All the classic method are provide such as list,create,retrieve,update,partial_update, destroy

    @action(detail=True, methods=[HTTPMethod.POST], url_path="plugins")
    def add_plugin(self, request, pk=None):
        server = get_object_or_404(Server, pk=pk)
        serializer = ServerPluginSerializer(
            data=request.data, context={"server": server}
        )

        if serializer.is_valid():
            serializer.save()
            return self.success_response("Plugin added to server successfully", server)

        return self.error_response("Error during plugin adding", serializer.errors)
