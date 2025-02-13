from drf_spectacular.views import SpectacularAPIView
from rest_framework.permissions import IsAdminUser


class RestrictedSpectacularAPIView(SpectacularAPIView):
    permission_classes = [IsAdminUser]
