from rest_framework import generics
from rest_framework.permissions import AllowAny

from .serializers import RegisterSerializer


class RegisterView(generics.CreateAPIView):
    """Create a new user account.

    POST /api/auth/register/  {"username": "...", "password": "...", "email": "..."}
    """

    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

