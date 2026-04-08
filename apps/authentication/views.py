from drf_spectacular.utils import extend_schema
from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .serializers import (
    EmailTokenObtainPairSerializer,
    RegisterSerializer,
    UserPublicSerializer,
)


def _tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }


@extend_schema(
    summary="Register",
    description="Create a new account. Returns user profile and JWT pair.",
    responses={201: UserPublicSerializer},
)
class RegisterView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        payload = {
            "user": UserPublicSerializer(user).data,
            **_tokens_for_user(user),
        }
        return Response(payload, status=status.HTTP_201_CREATED)


@extend_schema(
    summary="Login",
    description="Obtain JWT access and refresh tokens using email and password.",
)
class LoginView(TokenObtainPairView):
    permission_classes = [AllowAny]
    serializer_class = EmailTokenObtainPairSerializer


@extend_schema(summary="Refresh token")
class RefreshTokenView(TokenRefreshView):
    permission_classes = [AllowAny]
