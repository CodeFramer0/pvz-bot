from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema_view

from ..models import TelegramUser
from ..serializers.telegram_users import (
    TelegramUserSerializer,
    TelegramUserListSerializer,
    TelegramUserDetailSerializer,
)
from ..schemas.telegram_users import (
    telegram_users_list_schema,
    telegram_users_retrieve_schema,
    telegram_users_create_schema
)

@extend_schema_view(
    list=telegram_users_list_schema,
    retrieve=telegram_users_retrieve_schema,
    create=telegram_users_create_schema,
)
class TelegramUserViewSet(viewsets.ModelViewSet):
    queryset = TelegramUser.objects.all().order_by("id")
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        if self.action == "list":
            return TelegramUserListSerializer
        elif self.action == "retrieve":
            return TelegramUserDetailSerializer
        return TelegramUserSerializer