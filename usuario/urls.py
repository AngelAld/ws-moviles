from django.urls import path, include
from .views import (
    LoginView,
    LogoutAdminViewSet,
    LogoutViewSet,
    StatusClienteViewSet,
    TipoDocViewSet,
)
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

router = DefaultRouter()
router.register(r"logout", LogoutViewSet, basename="logout")
router.register(r"admin-logout", LogoutAdminViewSet, basename="admin-logout")
router.register(r"status", StatusClienteViewSet, basename="status")
router.register(r"tipo-doc", TipoDocViewSet, basename="tipo-doc")
urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("token-refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("", include(router.urls)),
]
