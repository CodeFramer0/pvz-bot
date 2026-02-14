"""
robot/serializers/__init__.py

Импортирует все сериализаторы из отдельных модулей
"""
from .auth import (
    EmailPasswordTokenObtainPairSerializer,
    UsernamePasswordTokenObtainPairSerializer,
    UserSerializer,
    UserCreateSerializer,
    UserDetailSerializer,
)

from .orders import (
    OrderListSerializer,
    OrderDetailSerializer,
    OrderCreateSerializer,
    OrderUpdateSerializer,
)

from .pickup_points import (
    PickupPointSerializer,
    PickupPointListSerializer,
    PickupPointDetailSerializer,
)

from .telegram_users import (
    TelegramUserSerializer,
    TelegramUserListSerializer,
    TelegramUserDetailSerializer,
)

__all__ = [
    # Auth Serializers
    'EmailPasswordTokenObtainPairSerializer',
    'UsernamePasswordTokenObtainPairSerializer',
    'UserSerializer',
    'UserCreateSerializer',
    'UserDetailSerializer',
    
    # Order Serializers
    'OrderListSerializer',
    'OrderDetailSerializer',
    'OrderCreateSerializer',
    'OrderUpdateSerializer',
    
    # PickupPoint Serializers
    'PickupPointSerializer',
    'PickupPointListSerializer',
    'PickupPointDetailSerializer',
    
    # TelegramUser Serializers
    'TelegramUserSerializer',
    'TelegramUserListSerializer',
    'TelegramUserDetailSerializer',
]
