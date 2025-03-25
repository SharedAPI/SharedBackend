from rest_framework import viewsets

from api.models.server import Server
from api.serializers.server import ServerSerializer
from api.utils import CustomResponseHandler


class ServerViewSet(viewsets.ModelViewSet, CustomResponseHandler):
    queryset = Server.objects.all()
    serializer_class = ServerSerializer
    # All the classic method are provide such as list,create,retrieve,update,partial_update, destroy
