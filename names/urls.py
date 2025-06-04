from django.urls import path
from .views import NameLookupView, PopularNamesView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView


urlpatterns = [
    path("names/predict/", NameLookupView.as_view(), name="name-prediction"),
    path("names/lookup/", NameLookupView.as_view(), name="name-lookup"),
    path("popular-names/", PopularNamesView.as_view(), name="popular-names"),
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path("docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),

]
