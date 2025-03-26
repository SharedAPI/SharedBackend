from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from api.models.plugin import PluginVersion
from api.models.server import Server
from api.serializers.plugin import DeprecatedPluginVersionSerializer, ReadOnlyPluginVersionSerializer, AddPluginSerializer
from api.utils import CustomResponseHandler


class DeprecatedPluginVersionView(APIView, CustomResponseHandler):
    @swagger_auto_schema(request_body=DeprecatedPluginVersionSerializer)
    def put(self, request, plugin_version_id=None):
        # Attempt to fetch a server by its UUID
        plugin_version = get_object_or_404(PluginVersion, pk=plugin_version_id)

        deprecation = DeprecatedPluginVersionSerializer(data=request.data)
        if not deprecation.is_valid():
            return self.error_response("Error during plugin deprecation serialization", deprecation.errors)

        plugin_version.deprecated = deprecation.validated_data.get("deprecated", False) # type: ignore
        plugin_version.save()

        return self.success_response(f"Deprecation of Plugin Version is done", plugin_version, status.HTTP_200_OK)
