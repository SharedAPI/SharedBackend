from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from ..models.plugin import Plugin

from ..serializers.plugin import PluginSerializer
from ..serializers.schema import SchemaSerializer


class PluginViewSet(viewsets.ModelViewSet):
    queryset = Plugin.objects.all()
    serializer_class = PluginSerializer

    @action(detail=True, methods=['post'])
    def create_schema(self, request, pk=None):
        serializer = SchemaSerializer(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            schema = serializer.data["schema"]

            return Response({'schema': schema})
        else:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
