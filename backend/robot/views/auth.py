from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils.crypto import get_random_string
from django_redis import get_redis_connection
from drf_spectacular.utils import extend_schema_view
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from ..models import AppUser
from ..schemas.auth import (change_password_schema, current_user_schema,
                            email_login_schema, logout_schema,
                            refresh_token_schema,
                            send_verification_code_schema,
                            username_login_schema, verify_code_schema,
                            verify_token_schema)
from ..serializers import (EmailPasswordTokenObtainPairSerializer,
                           UserSerializer)
from ..utils import generate_numeric_code, send_verification_email

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


class SendVerificationCodeView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        email = request.data.get("email")
        if not email:
            return Response({"email": "Обязательное поле"}, status=400)

        code = generate_numeric_code(6)

        r = get_redis_connection("default")
        key = f"email_verification:{email}"
        r.setex(key, 300, code)

        send_verification_email(email, code)

        return Response({"detail": "Код отправлен"}, status=200)


@extend_schema_view(post=verify_code_schema)
class VerifyCodeView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        email = request.data.get("email")
        code = request.data.get("code")

        if not email or not code:
            return Response({"detail": "email и code обязательны"}, status=400)

        r = get_redis_connection("default")

        code_key = f"email_verification:{email}"
        saved_code = r.get(code_key)

        if not saved_code:
            return Response({"detail": "Код истёк или не найден"}, status=400)

        if saved_code.decode() != code:
            return Response({"detail": "Неверный код"}, status=400)

        # одноразовый temp token (на биндинг / установку пароля)
        temp_token = get_random_string(48)
        token_key = f"email_verification_token:{email}"

        r.setex(token_key, 600, temp_token)  # 10 минут
        r.delete(code_key)  # код больше нельзя использовать

        return Response({"temporary_token": temp_token}, status=status.HTTP_200_OK)


class ForgotPasswordView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        email = request.data.get("email")
        if not email:
            return Response({"email": "Обязательное поле"}, status=400)

        user = AppUser.objects.filter(email=email).first()
        if not user:
            # Всегда возвращаем одинаковый ответ → безопасность
            return Response(
                {"detail": "Если email зарегистрирован, ссылка отправлена"}, status=200
            )

        # создаём одноразовый reset токен в Redis
        token = get_random_string(48)
        r = get_redis_connection("default")
        key = f"password_reset:{email}"
        r.setex(key, 600, token)  # 10 минут TTL

        reset_link = f"http://pvz.localhost/reset-password?code={token}"

        # Отправляем email (HTML вариант)
        send_verification_email(
            email,
            f"Сброс пароля",
            html=f"""
            <html>
              <body style="font-family: Arial; text-align: center;">
                <h2>Сброс пароля</h2>
                <p>Для сброса пароля нажмите на кнопку ниже:</p>
                <a href="{reset_link}" style="display:inline-block;padding:10px 20px;
                   background:#1a73e8;color:white;border-radius:5px;text-decoration:none;">
                   Сбросить пароль
                </a>
                <p>Ссылка действительна 10 минут.</p>
              </body>
            </html>
            """,
        )

        return Response(
            {"detail": "Если email зарегистрирован, ссылка отправлена"}, status=200
        )


class ResetPasswordView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        email = request.data.get("email")
        token = request.data.get("code")  # одноразовый токен из письма
        new_password = request.data.get("new_password")
        new_password_confirm = request.data.get("new_password_confirm")

        if not email or not token:
            return Response({"detail": "email и code обязательны"}, status=400)

        r = get_redis_connection("default")
        key = f"password_reset:{email}"
        saved_token = r.get(key)

        if not saved_token or saved_token.decode() != token:
            return Response({"detail": "Неверный код или срок истёк"}, status=400)

        if new_password != new_password_confirm:
            return Response({"detail": "Пароли не совпадают"}, status=400)
        if len(new_password) < 8:
            return Response(
                {"detail": "Пароль должен быть минимум 8 символов"}, status=400
            )

        user = AppUser.objects.filter(email=email).first()
        if not user:
            return Response({"detail": "Пользователь не найден"}, status=400)

        user.set_password(new_password)
        user.save(update_fields=["password"])

        r.delete(key)  # токен одноразовый, удаляем

        return Response({"detail": "Пароль успешно изменён"}, status=200)
