from django.urls import include, path
from rest_framework import routers

from api.views.add_plugin import ServersPluginManagementView
from api.views.deprecated_version import DeprecatedPluginVersionView
from api.viewsets.plugin import PluginViewSet
from api.viewsets.server import ServerViewSet

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()

router.register(r"plugins", PluginViewSet, basename="plugins")
router.register(r"servers", ServerViewSet, basename="servers")


urlpatterns = [
    path("", include(router.urls)),
    path(
        "versions/<uuid:plugin_version_id>/deprecated",
        DeprecatedPluginVersionView.as_view(),
        name="plugin_versions_deprecation",
    ),
    path(
        "servers/<uuid:server_id>/plugins",
        ServersPluginManagementView.as_view(),
        name="servers_plugin_management",
    ),
]
