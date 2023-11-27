from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CargaViewSet,
    HistorialCargaViewSet,
    AnularCargaViewSet,
    EstadoCargaViewSet,
    AsignarVehiculoViewSet,
)

router = DefaultRouter()

router.register("carga", CargaViewSet, basename="carga")
router.register("estado-carga", EstadoCargaViewSet, basename="estado-carga")
router.register("historial-carga", HistorialCargaViewSet, basename="historial-carga")
router.register("anular-carga", AnularCargaViewSet, basename="anular-carga")
router.register("asignar-vehiculo", AsignarVehiculoViewSet, basename="asignar-vehiculo")

urlpatterns = [
    path("", include(router.urls)),
]
