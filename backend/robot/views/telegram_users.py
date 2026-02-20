from django.contrib.auth import get_user_model
from django.utils.crypto import get_random_string
from drf_spectacular.utils import extend_schema_view
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from ..filters import TelegramUserFilter
from ..models import TelegramUser
from ..schemas.telegram_users import (telegram_users_bind_user_schema,
                                      telegram_users_create_schema,
                                      telegram_users_destroy_schema,
                                      telegram_users_list_schema,
                                      telegram_users_retrieve_schema,
                                      telegram_users_update_schema)
from ..serializers.telegram_users import TelegramUserSerializer

AppUser = get_user_model()


@extend_schema_view(
    list=telegram_users_list_schema,
    retrieve=telegram_users_retrieve_schema,
    create=telegram_users_create_schema,
    update=telegram_users_update_schema,
    partial_update=telegram_users_update_schema,
    destroy=telegram_users_destroy_schema,
)
class TelegramUserViewSet(viewsets.ModelViewSet):
    """
    CRUD TelegramUser + bind_user action
    """

    queryset = TelegramUser.objects.all().select_related("app_user").order_by("id")
    permission_classes = (IsAuthenticated,)
    filterset_class = TelegramUserFilter
    serializer_class = TelegramUserSerializer

    @telegram_users_bind_user_schema
    @action(detail=True, methods=["post"])
    def bind_user(self, request, pk=None):
        telegram_user = self.get_object()
        email = request.data.get("email")

        if not email:
            return Response({"email": "Обязательное поле"}, status=400)

        if AppUser.objects.filter(email=email).exists():
            return Response(
                {"email": "Пользователь с таким email уже существует"}, status=400
            )

        # сгенерировать username на базе TG ID или случайный
        username = f"tg_{telegram_user.user_id}_{get_random_string(5)}"

        password = get_random_string(12)
        user = AppUser.objects.create_user(
            username=username, email=email, password=password
        )

        telegram_user.app_user = user
        telegram_user.save(update_fields=["app_user"])

        return Response(
            {"id": user.id, "email": user.email, "password": password}, status=200
        )
