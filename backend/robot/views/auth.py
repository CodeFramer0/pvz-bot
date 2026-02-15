from django.utils.crypto import get_random_string
from drf_spectacular.utils import extend_schema_view
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView

from ..models import AppUser
from ..schemas.auth import (change_password_schema, current_user_schema,
                            email_login_schema, logout_schema,
                            refresh_token_schema,
                            send_verification_code_schema,
                            username_login_schema, verify_code_schema,
                            verify_token_schema)
from ..serializers import (EmailPasswordTokenObtainPairSerializer,
                           UserSerializer)

# ================= VERIFICATION CODES =================
verification_store = {}  # для простоты, в проде Redis/DB
password_reset_store = {}
from django.contrib.auth import get_user_model

AppUser = get_user_model()

import logging

logger = logging.getLogger(__name__)


class EmailTokenObtainPairView(TokenObtainPairView):
    """
    Логин по email и password с выдачей access и refresh токенов
    """
    permission_classes = (AllowAny,)
    serializer_class = EmailPasswordTokenObtainPairSerializer


@extend_schema_view(get=current_user_schema)
class CurrentUserView(APIView):
    permission_classes = (IsAuthenticated,)

    @action(detail=True, methods=["POST"])
    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

@extend_schema_view(post=refresh_token_schema)
class RefreshTokenView(TokenRefreshView):
    permission_classes = (AllowAny,)


@extend_schema_view(post=logout_schema)
class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    @action(detail=True, methods=["POST"])
    def post(self, request):
        refresh_token = request.data.get("refresh")
        if not refresh_token:
            return Response(
                {"detail": "Refresh token is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(
                {"detail": "Successfully logged out"}, status=status.HTTP_200_OK
            )
        except TokenError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@extend_schema_view(post=change_password_schema)
class ChangePasswordView(APIView):
    permission_classes = (IsAuthenticated,)

    @action(detail=True, methods=["POST"])
    def post(self, request):
        user = request.user
        old_password = request.data.get("old_password")
        new_password = request.data.get("new_password")
        new_password_confirm = request.data.get("new_password_confirm")

        if not user.check_password(old_password):
            return Response(
                {"old_password": "Wrong password"}, status=status.HTTP_400_BAD_REQUEST
            )
        if new_password != new_password_confirm:
            return Response(
                {"new_password": "Passwords do not match"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if len(new_password) < 8:
            return Response(
                {"new_password": "Password must be at least 8 characters"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user.set_password(new_password)
        user.save()
        return Response(
            {"detail": "Password changed successfully"}, status=status.HTTP_200_OK
        )


@extend_schema_view(post=verify_token_schema)
class VerifyTokenView(APIView):
    permission_classes = (AllowAny,)

    @action(detail=True, methods=["POST"])
    def post(self, request):
        token = request.data.get("token")
        if not token:
            return Response(
                {"valid": False, "detail": "Token is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            AccessToken(token)
            return Response({"valid": True}, status=status.HTTP_200_OK)
        except TokenError as e:
            return Response(
                {"valid": False, "detail": str(e)}, status=status.HTTP_400_BAD_REQUEST
            )


@extend_schema_view(post=send_verification_code_schema)
class SendVerificationCodeView(APIView):
    permission_classes = (AllowAny,)

    @action(detail=True, methods=["POST"])
    def post(self, request):
        email = request.data.get("email")
        if not email:
            return Response({"email": "Обязательное поле"}, status=400)

        code = get_random_string(6, allowed_chars="0123456789")
        verification_store[email] = code  # + TTL в проде
        print(f"Verification code for {email}: {code}")  # сюда вставить email-сервис
        return Response({"detail": "Код отправлен"}, status=200)


@extend_schema_view(post=verify_code_schema)
class VerifyCodeView(APIView):
    permission_classes = (AllowAny,)

    @action(detail=True, methods=["POST"])
    def post(self, request):
        email = request.data.get("email")
        code = request.data.get("code")
        if verification_store.get(email) != code:
            return Response({"detail": "Неверный код"}, status=400)

        temp_token = get_random_string(32)
        verification_store[email] = {"verified": True, "temp_token": temp_token}
        return Response({"temporary_token": temp_token}, status=200)


# можно создать свой schema
class ForgotPasswordView(APIView):
    permission_classes = (AllowAny,)

    @action(detail=True, methods=["POST"])
    def post(self, request):
        email = request.data.get("email")
        if not email:
            return Response({"email": "Обязательное поле"}, status=400)

        user = AppUser.objects.filter(email=email).first()
        if not user:
            return Response(
                {"detail": "Если email зарегистрирован, ссылка отправлена"}, status=200
            )

        code = get_random_string(32)
        password_reset_store[email] = code

        reset_link = f"http://pvz.localhost/reset-password?code={code}"
        print(reset_link)

        return Response(
            {"detail": "Если email зарегистрирован, ссылка отправлена"}, status=200
        )


class ResetPasswordView(APIView):
    permission_classes = (AllowAny,)

    @action(detail=True, methods=["POST"])
    def post(self, request):
        email = request.data.get("email")
        code = request.data.get("code")
        new_password = request.data.get("new_password")
        new_password_confirm = request.data.get("new_password_confirm")

        if password_reset_store.get(email) != code:
            return Response({"detail": "Неверный код"}, status=400)

        if new_password != new_password_confirm:
            return Response({"detail": "Пароли не совпадают"}, status=400)

        user = AppUser.objects.filter(email=email).first()
        if not user:
            return Response({"detail": "Пользователь не найден"}, status=400)

        user.set_password(new_password)
        user.save()
        del password_reset_store[email]

        return Response({"detail": "Пароль успешно изменён"}, status=200)
