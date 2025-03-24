from django.urls import include, path
from rest_framework import routers

from api.viewsets.plugin import PluginViewSet

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()

router.register(r"plugins", PluginViewSet, basename="plugins")


urlpatterns = [
    path("", include(router.urls)),
]
