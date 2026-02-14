from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.views import TokenRefreshView
from drf_spectacular.utils import extend_schema_view

from ..serializers import EmailPasswordTokenObtainPairSerializer, UsernamePasswordTokenObtainPairSerializer, UserSerializer
from ..schemas.auth import (
    email_login_schema,
    username_login_schema,
    refresh_token_schema,
    logout_schema,
    current_user_schema,
    change_password_schema,
    verify_token_schema,
)


@extend_schema_view(post=email_login_schema)
class EmailPasswordLoginView(APIView):
    permission_classes = (AllowAny,)
    def post(self, request):
        serializer = EmailPasswordTokenObtainPairSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)


@extend_schema_view(post=username_login_schema)
class UsernamePasswordLoginView(APIView):
    permission_classes = (AllowAny,)
    def post(self, request):
        serializer = UsernamePasswordTokenObtainPairSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)


@extend_schema_view(post=refresh_token_schema)
class RefreshTokenView(TokenRefreshView):
    permission_classes = (AllowAny,)


@extend_schema_view(post=logout_schema)
class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request):
        refresh_token = request.data.get('refresh')
        if not refresh_token:
            return Response({"detail": "Refresh token is required"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"detail": "Successfully logged out"}, status=status.HTTP_200_OK)
        except TokenError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@extend_schema_view(get=current_user_schema)
class CurrentUserView(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


@extend_schema_view(post=change_password_schema)
class ChangePasswordView(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request):
        user = request.user
        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')
        new_password_confirm = request.data.get('new_password_confirm')

        if not user.check_password(old_password):
            return Response({"old_password": "Wrong password"}, status=status.HTTP_400_BAD_REQUEST)
        if new_password != new_password_confirm:
            return Response({"new_password": "Passwords do not match"}, status=status.HTTP_400_BAD_REQUEST)
        if len(new_password) < 8:
            return Response({"new_password": "Password must be at least 8 characters"}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password)
        user.save()
        return Response({"detail": "Password changed successfully"}, status=status.HTTP_200_OK)


@extend_schema_view(post=verify_token_schema)
class VerifyTokenView(APIView):
    permission_classes = (AllowAny,)
    def post(self, request):
        token = request.data.get('token')
        if not token:
            return Response({"valid": False, "detail": "Token is required"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            AccessToken(token)
            return Response({"valid": True}, status=status.HTTP_200_OK)
        except TokenError as e:
            return Response({"valid": False, "detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
