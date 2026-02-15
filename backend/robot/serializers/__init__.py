"""
robot/serializers/__init__.py

Импортирует все сериализаторы из отдельных модулей
"""

from .users import (EmailPasswordTokenObtainPairSerializer,
                   UserCreateSerializer, UserDetailSerializer,
                   UsernamePasswordTokenObtainPairSerializer, UserSerializer)
from .orders import (OrderCreateSerializer, OrderDetailSerializer,
                     OrderListSerializer, OrderUpdateSerializer)
from .pickup_points import (PickupPointDetailSerializer,
                            PickupPointListSerializer, PickupPointSerializer)
from .telegram_users import (TelegramUserDetailSerializer,
                             TelegramUserListSerializer,
                             TelegramUserSerializer)

__all__ = [
    # Auth Serializers
    "EmailPasswordTokenObtainPairSerializer",
    "UsernamePasswordTokenObtainPairSerializer",
    "UserSerializer",
    "UserCreateSerializer",
    "UserDetailSerializer",
    # Order Serializers
    "OrderListSerializer",
    "OrderDetailSerializer",
    "OrderCreateSerializer",
    "OrderUpdateSerializer",
    # PickupPoint Serializers
    "PickupPointSerializer",
    "PickupPointListSerializer",
    "PickupPointDetailSerializer",
    # TelegramUser Serializers
    "TelegramUserSerializer",
    "TelegramUserListSerializer",
    "TelegramUserDetailSerializer",
]
