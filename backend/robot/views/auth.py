from django.contrib.auth import get_user_model
from django.utils.crypto import get_random_string
from django_redis import get_redis_connection
from drf_spectacular.utils import extend_schema
from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.parsers import FormParser, MultiPartParser, JSONParser
from ..serializers.auth import (
    EmailPasswordTokenObtainPairSerializer,
    EmailSerializer,
    ResetPasswordSerializer,
    VerifyCodeSerializer,
    VerifyTokenSerializer,
    LogoutSerializer
)

AppUser = get_user_model()

@extend_schema(tags=["Auth"], summary="Логин (получение JWT)")
class EmailTokenObtainPairView(TokenObtainPairView):
    serializer_class = EmailPasswordTokenObtainPairSerializer
    parser_classes = [JSONParser, FormParser, MultiPartParser]


@extend_schema(tags=["Auth"], summary="Обновление JWT (refresh)")
class RefreshTokenView(TokenRefreshView):
    pass


@extend_schema(
    tags=["Auth"], 
    summary="Выход из системы", 
    description="Добавляет refresh токен в черный список (Blacklist)"
)
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    @extend_schema(
        request=LogoutSerializer, # Теперь Swagger знает, что нужно поле refresh
        responses={205: None},
        tags=["Auth"]
    )
    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"detail": "Logged out"}, status=status.HTTP_205_RESET_CONTENT)
        except Exception:
            return Response(
                {"detail": "Invalid token or already blacklisted"}, 
                status=status.HTTP_400_BAD_REQUEST
            )


@extend_schema(
    tags=["Auth: Password Reset"],
    summary="1. Отправить код на Email",
    description="Генерирует 6-значный код и сохраняет в Redis на 5 минут."
)
class SendVerificationCodeView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = EmailSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data["email"]
        
        code = get_random_string(6, allowed_chars="0123456789")
        r = get_redis_connection("default")
        r.setex(f"email_verif:{email}", 300, code)
        
        # Здесь должна быть логика отправки письма: send_mail(...)
        return Response({"detail": "Код отправлен на указанный email"})


@extend_schema(
    tags=["Auth: Password Reset"],
    summary="2. Проверить код",
    description="Проверяет код из Redis и выдает временный токен для сброса пароля."
)
class VerifyCodeView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = VerifyCodeSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        email = serializer.validated_data["email"]
        code = serializer.validated_data["code"]

        r = get_redis_connection("default")
        saved_code = r.get(f"email_verif:{email}")
        
        if not saved_code or saved_code.decode() != code:
            return Response({"detail": "Неверный или истекший код"}, status=status.HTTP_400_BAD_REQUEST)

        temp_token = get_random_string(48)
        # Сохраняем токен для финального шага смены пароля
        r.setex(f"password_reset_token:{email}", 600, temp_token)
        r.delete(f"email_verif:{email}")
        
        return Response({"temporary_token": temp_token})


@extend_schema(
    tags=["Auth: Password Reset"],
    summary="3. Установить новый пароль",
    description="Финальный шаг: принимает временный токен из шага №2 и меняет пароль пользователя."
)
class ResetPasswordView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = ResetPasswordSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        token = serializer.validated_data["code"] # Это temp_token из шага 2
        
        r = get_redis_connection("default")
        saved_token = r.get(f"password_reset_token:{email}")
        
        if not saved_token or saved_token.decode() != token:
            return Response({"detail": "Токен истек или недействителен"}, status=status.HTTP_400_BAD_REQUEST)

        user = AppUser.objects.filter(email=email).first()
        if not user:
            return Response({"detail": "Пользователь не найден"}, status=status.HTTP_404_NOT_FOUND)

        user.set_password(serializer.validated_data["new_password"])
        user.save()
        r.delete(f"password_reset_token:{email}")
        
        return Response({"detail": "Пароль успешно изменен"})


@extend_schema(
    tags=["Auth: Utils"],
    summary="Проверить валидность Access токена",
    description="Проверяет, не протух ли JWT токен."
)
class VerifyTokenView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = VerifyTokenSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            AccessToken(serializer.validated_data["token"])
            return Response({"valid": True})
        except Exception as e:
            return Response({"valid": False, "detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
