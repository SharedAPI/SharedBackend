from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.views import APIView

from api.models.server import Server
from api.serializers.plugin import PluginSerializer
from api.serializers.server import AddPluginSerializer
from api.utils import CustomResponseHandler


class ServersPluginManagementView(APIView, CustomResponseHandler):
    def get(self, request, server_id=None):
        # Attempt to fetch a server by its UUID
        server = Server.objects.get(id=server_id)
        if not server.plugins:
            return JsonResponse(
                {"message": "No plugins found for the given server"},
                status=status.HTTP_200_OK,
            )

        serialized_plugins = PluginSerializer(server.plugins, many=True)

        return JsonResponse(
            {
                "message": f"List of plugin for server: {server_id}",
                "objects": str(serialized_plugins.data),
            },
            status=status.HTTP_200_OK,
        )

    @swagger_auto_schema(request_body=AddPluginSerializer)
    def post(self, request, server_id=None):
        # Handle the POST logic here if needed
        server = get_object_or_404(Server, pk=server_id)

        serializer = AddPluginSerializer(data=request.data, context={"server": server})
        if serializer.is_valid():
            serializer.save()
            return self.success_response("Plugin added to server successfully", server)

        return self.error_response("Error during plugin adding", serializer.errors)
