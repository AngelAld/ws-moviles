from rest_framework.routers import DefaultRouter
from .views import ConfigViewSet
from django.urls import path, include

router = DefaultRouter()

router.register("config", ConfigViewSet, basename="config")


urlpatterns = [
    path("", include(router.urls)),
]
