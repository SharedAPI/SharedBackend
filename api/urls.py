from django.urls import include, path
from rest_framework import routers

from api.viewsets.plugin import PluginViewSet
from api.viewsets.server import ServerViewSet

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()

router.register(r"plugins", PluginViewSet, basename="plugins")
router.register(r"servers", ServerViewSet, basename="servers")


urlpatterns = [
    path("", include(router.urls)),
]
