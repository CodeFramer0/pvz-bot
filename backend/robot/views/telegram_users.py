from django.utils.crypto import get_random_string
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from ..filters import TelegramUserFilter
from ..models import AppUser, TelegramUser
from ..serializers.telegram_users import TelegramUserSerializer
from django.db import transaction, IntegrityError
from rest_framework import status
from rest_framework.response import Response

@extend_schema_view(
    list=extend_schema(summary="Список пользователей Telegram", tags=["Telegram Users"]),
    retrieve=extend_schema(summary="Детальная информация о TG пользователе", tags=["Telegram Users"]),
    create=extend_schema(summary="Создать запись TG пользователя", tags=["Telegram Users"]),
    update=extend_schema(summary="Полное обновление TG пользователя", tags=["Telegram Users"]),
    partial_update=extend_schema(summary="Частичное обновление TG пользователя", tags=["Telegram Users"]),
    destroy=extend_schema(summary="Удалить TG пользователя", tags=["Telegram Users"]),
)
class TelegramUserViewSet(viewsets.ModelViewSet):
    """
    Управление пользователями Telegram и их связкой с аккаунтами системы.
    """
    queryset = TelegramUser.objects.all().select_related("app_user").order_by("id")
    permission_classes = (IsAuthenticated,)
    filterset_class = TelegramUserFilter
    serializer_class = TelegramUserSerializer
    
    @extend_schema(
    summary="Upsert Telegram пользователя по user_id",
    description="Создает TelegramUser, если его нет, либо обновляет name/nick_name по user_id. Идемпотентный эндпоинт.",
    tags=["Telegram Users"],
    request={
        "application/json": {
            "type": "object",
            "properties": {
                "user_id": {"type": "string", "description": "Telegram user_id"},
                "name": {"type": "string"},
                "nick_name": {"type": "string"},
            },
            "required": ["user_id"],
        }
    },
    responses={
        201: {
            "description": "Создан новый TelegramUser",
        },
        200: {
            "description": "TelegramUser обновлён или уже существовал",
        },
        400: {"description": "user_id не передан"},
        409: {"description": "Конфликт уникальности (редкий race condition)"},
    },
)
    def create(self, request, *args, **kwargs):
        user_id = request.data.get("user_id")
        if not user_id:
            return Response({"user_id": "Обязательное поле"}, status=400)

        try:
            with transaction.atomic():
                obj, created = TelegramUser.objects.update_or_create(
                    user_id=str(user_id),
                    defaults={
                        "name": request.data.get("name", "NoName"),
                        "nick_name": request.data.get("nick_name", "NoName"),
                    },
                )
        except IntegrityError:
            obj = TelegramUser.objects.get(user_id=str(user_id))
            created = False

        serializer = self.get_serializer(obj)
        return Response(serializer.data, status=status.HTTP_200_OK if not created else status.HTTP_201_CREATED)

    @extend_schema(
        summary="Привязать аккаунт (регистрация через TG)",
        description="Создает системного пользователя (AppUser) на основе email и привязывает его к записи Telegram.",
        request={"application/json": {
            "type": "object",
            "properties": {"email": {"type": "string", "format": "email"}},
            "required": ["email"]
        }},
        responses={
            200: {
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "email": {"type": "string"},
                    "password": {"type": "string", "description": "Сгенерированный пароль"}
                }
            },
            400: {"description": "Email уже занят или не передан"}
        },
        tags=["Telegram Users: Actions"]
    )
    @action(detail=True, methods=["post"], url_path="bind-user")
    def bind_user(self, request, pk=None):
        telegram_user = self.get_object()
        email = request.data.get("email")

        if not email:
            return Response({"email": "Обязательное поле"}, status=status.HTTP_400_BAD_REQUEST)

        if AppUser.objects.filter(email=email).exists():
            return Response(
                {"email": "Пользователь с таким email уже существует"}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        # Генерация username и создание пользователя
        username = f"tg_{telegram_user.user_id}_{get_random_string(5)}"
        password = get_random_string(12)
        
        user = AppUser.objects.create_user(
            username=username, 
            email=email, 
            password=password
        )

        telegram_user.app_user = user
        telegram_user.save(update_fields=["app_user"])

        return Response(
            {"id": user.id, "email": user.email, "password": password}, 
            status=status.HTTP_200_OK
        )
