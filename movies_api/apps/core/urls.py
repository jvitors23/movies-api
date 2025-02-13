from django.urls import path
from drf_spectacular.views import SpectacularRedocView, SpectacularSwaggerView

from movies_api.apps.core.views import RestrictedSpectacularAPIView

urlpatterns_documentation = [
    path("api/schema/", RestrictedSpectacularAPIView.as_view(), name="schema"),
    path("api/schema/swagger-ui/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("api/schema/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
]


urlpatterns = [] + urlpatterns_documentation
