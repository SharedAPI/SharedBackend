from rest_framework import status, viewsets
from rest_framework.response import Response

from ..serializers.schema import SchemaSerializer


class SchemaViewSet(viewsets.ViewSet):
    serializer_class = SchemaSerializer

    def create(self, request, pk=None):
        if request.method != "POST":
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

        serializer = SchemaSerializer(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            schema = serializer.data["schema"]

            return Response({'schema': schema})
        else:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
