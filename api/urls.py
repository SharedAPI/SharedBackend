from django.urls import include, path
from rest_framework import routers

from .viewsets.server import ServerViewSet, ServerPluginsViewSet
from .viewsets.plugin import PluginViewSet
from .viewsets.schema import SchemaViewSet

from .views import schema

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r"auth", ServerPluginsViewSet)
router.register(r"servers", ServerViewSet)
router.register(r"plugins", PluginViewSet)

router.register("api/schema/<uuid:plugin_uuid>", SchemaViewSet, basename="schema")


urlpatterns = [
    path("", include(router.urls)),
]
