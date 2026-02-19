"""
robot/serializers/__init__.py

Импортирует все сериализаторы из отдельных модулей
"""

from .auth import EmailPasswordTokenObtainPairSerializer
from .orders import (
    OrderCreateSerializer,
    OrderDetailSerializer,
    OrderListSerializer,
    OrderUpdateSerializer,
)
from .pickup_points import (
    PickupPointDetailSerializer,
    PickupPointListSerializer,
    PickupPointSerializer,
)
from .telegram_users import TelegramUserSerializer
from .users import UserSerializer

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
