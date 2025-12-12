from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)
from rest_framework import permissions
from config.health import HealthCheckView




urlpatterns = [
    path("health/", HealthCheckView.as_view(), name="health"),
    path("admin/", admin.site.urls),
    # API Documentation
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "swagger/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path("redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
    path("api/v1/", include("properties.urls")),
    # user urls
    path("api/v1/users/", include("users.urls")),
]


# Serve media files during development and production
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
else:
    # For production, still add media URLs (static files handled by web server)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
