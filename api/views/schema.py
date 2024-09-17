from rest_framework import status
from rest_framework.response import Response

from django.views.decorators.http import require_POST

from ..serializers.schema import SchemaSerializer


@require_POST
def create_schema(request, plugin_uuid=None):
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