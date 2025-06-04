from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from drf_spectacular.utils import extend_schema
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


@extend_schema(
    tags=["auth"],
    request=TokenObtainPairSerializer,
    responses={
        200: {
            "type": "object",
            "properties": {
                "access": {"type": "string"},
                "refresh": {"type": "string"},
            },
        }
    },
    description=(
        "Send JSON with username and password to receive access and refresh tokens.\n\n"
        "Example:\n{\n  \"username\": \"admin\",\n  \"password\": \"admin123\"\n}"
    )
)
class CustomTokenObtainPairView(TokenObtainPairView):
    pass


urlpatterns = [
    # Admin
    path("admin/", admin.site.urls),

    # App routes
    path("", include("names.urls")),

    # JWT authentication
    path("api/token/", CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

    # API Schema & Docs
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path("docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
]

# Static files for admin panel (Jazzmin)
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
