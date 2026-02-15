from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema_view
from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from ..schemas.users import (users_create_schema, users_destroy_schema,
                             users_list_schema, users_retrieve_schema,
                             users_update_schema)
from ..serializers import UserCreateSerializer, UserSerializer

AppUser = get_user_model()
from django.contrib.auth import get_user_model
from django.utils.crypto import get_random_string
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from ..serializers.users import (UserVerificationConfirmSerializer,
                                UserVerificationSendSerializer)

User = get_user_model()


@extend_schema_view(
    list=users_list_schema,
    create=users_create_schema,
    retrieve=users_retrieve_schema,
    update=users_update_schema,
    partial_update=users_update_schema,  # ← PATCH /users/{id}/ тоже под Users
    destroy=users_destroy_schema,
)
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = None  # Будет меняться через get_serializer_class

    def get_serializer_class(self):
        if self.action == "send_verification":
            return UserVerificationSendSerializer
        if self.action == "verify_email":
            return UserVerificationConfirmSerializer
        return UserSerializer  # ваш основной сериализатор AppUser

    @action(detail=False, methods=["post"], url_path="send-verification")
    def send_verification(self, request):
        """
        Отправка кода подтверждения на email
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data["email"]

        # ищем пользователя
        user, created = User.objects.get_or_create(
            email=email, defaults={"username": email, "is_active": True}
        )

        # Генерим код
        code = get_random_string(6, allowed_chars="0123456789")
        user.verification_code = code
        user.is_verified = False
        user.save()

        # Тут должен быть вызов email-сервиса
        # send_email(email, code)
        print(f"[DEBUG] Verification code for {email}: {code}")

        return Response({"detail": "Код подтверждения отправлен"}, status=200)

    @action(detail=False, methods=["post"], url_path="verify-email")
    def verify_email(self, request):
        """
        Подтверждение email по коду
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data["email"]
        code = serializer.validated_data["code"]

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"email": "Пользователь не найден"}, status=404)

        if user.verification_code != code:
            return Response({"code": "Неверный код"}, status=400)

        user.is_verified = True
        user.verification_code = ""
        user.save()

        return Response({"detail": "Email подтвержден"}, status=200)
