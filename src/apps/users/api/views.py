from drf_spectacular.utils import extend_schema
from rest_framework import generics, permissions

from .serializers import UserRegistrationSerializer


@extend_schema(
    summary="User registration",
    description="Create a new user account.",
)
class UserRegistrationView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]
