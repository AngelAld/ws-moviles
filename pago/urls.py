from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import EstadoPagoViewSet, PagoViewSet, ConfirmarPagoViewSet

router = DefaultRouter()
router.register("estado-pago", EstadoPagoViewSet, basename="estado-pago")
router.register("pago", PagoViewSet, basename="pago")
router.register("confirmar-pago", ConfirmarPagoViewSet, basename="confirmar-pago")
urlpatterns = [
    path("", include(router.urls)),
]
