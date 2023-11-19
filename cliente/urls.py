from django.urls import path, include
from .views import ClienteViewSet, ClienteRegisterView, ClienteAdminViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("cliente", ClienteViewSet, basename="clientes")
router.register("cliente-admin", ClienteAdminViewSet, basename="cliente-admin")
router.register("cliente-register", ClienteRegisterView, basename="cliente-register")


urlpatterns = [path("", include(router.urls))]
