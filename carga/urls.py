from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CargaViewSet

router = DefaultRouter()

router.register("carga", CargaViewSet, basename="carga")

urlpatterns = [
    path("", include(router.urls)),
]
