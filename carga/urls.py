from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CargaViewSet,
    HistorialCargaViewSet,
    AnularCargaViewSet,
    EstadoCargaViewSet,
)

router = DefaultRouter()

router.register("carga", CargaViewSet, basename="carga")
router.register("estado-carga", EstadoCargaViewSet, basename="estado-carga")
router.register("historial-carga", HistorialCargaViewSet, basename="historial-carga")
router.register("anular-carga", AnularCargaViewSet, basename="anular-carga")
urlpatterns = [
    path("", include(router.urls)),
]
