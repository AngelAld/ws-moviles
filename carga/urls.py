from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CargaViewSet, CargaEstadoViewSet

router = DefaultRouter()

router.register("carga", CargaViewSet, basename="carga")
# router.register("historial-carga", HistorialCargaViewSet, basename="historial-carga")
router.register("estado-carga", CargaEstadoViewSet, basename="estado-carga")

urlpatterns = [
    path("", include(router.urls)),
]
