from rest_framework import generics, permissions

from movies_api.apps.users.serializers import UserSerializer


class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system"""

    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]
