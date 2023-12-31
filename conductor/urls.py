from django.urls import path, include
from .views import (
    ConductorViewSet,
    ConductorRegisterView,
    ConductorAdminViewSet,
    VehiculoViewSet,
    UbicacionViewSet,
    ReportarUbicacionView,
)
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("conductor", ConductorViewSet, basename="conductores")
router.register("conductor-admin", ConductorAdminViewSet, basename="conductor-admin")
router.register(
    "conductor-register", ConductorRegisterView, basename="conductor-register"
)
router.register("vehiculo", VehiculoViewSet, basename="vehiculos")
router.register("ubicacion", UbicacionViewSet, basename="ubicaciones")
router.register(
    "reportar-ubicacion", ReportarUbicacionView, basename="reportar-ubicacion"
)
urlpatterns = [path("", include(router.urls))]
