from django.urls import include, path
from rest_framework import routers

from .viewsets.server import ServerViewSet
from .viewsets.plugin import PluginViewSet


# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'servers', ServerViewSet)
router.register(r'plugins', PluginViewSet)


urlpatterns = [
    path('', include(router.urls)),
    
]