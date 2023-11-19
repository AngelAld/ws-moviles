from django.urls import path, include
from .views import ConductorViewSet, ConductorRegisterView, ConductorAdminViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("conductor", ConductorViewSet, basename="conductores")
router.register("conductor-admin", ConductorAdminViewSet, basename="conductor-admin")
router.register(
    "conductor-register", ConductorRegisterView, basename="conductor-register"
)


urlpatterns = [path("", include(router.urls))]
