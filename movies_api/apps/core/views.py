from drf_spectacular.views import SpectacularAPIView


class RestrictedSpectacularAPIView(SpectacularAPIView):
    permission_classes = []
