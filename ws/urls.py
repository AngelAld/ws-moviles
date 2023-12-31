"""
URL configuration for ws project.
"""
from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("admin/", admin.site.urls),
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path(
        "alter-docs/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="Redoc-ui",
    ),
    path("usuario/", include("usuario.urls")),
    path("cliente/", include("cliente.urls")),
    path("conductor/", include("conductor.urls")),
    path("carga/", include("carga.urls")),
    path("pago/", include("pago.urls")),
    path("config/", include("customConfig.urls")),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
