"""
robot/serializers/__init__.py
Точка сборки всех сериализаторов приложения
"""

from .auth import (
    EmailPasswordTokenObtainPairSerializer,
    ChangePasswordSerializer,
    EmailSerializer,
    VerifyCodeSerializer,
    ResetPasswordSerializer,
    VerifyTokenSerializer,
    LogoutSerializer,
)
from .marketplaces import MarketplaceSerializer
from .news_letters import NewsletterSerializer
from .orders import (
    OrderCreateSerializer,
    OrderDetailSerializer,
    OrderListSerializer,
)
from .pickup_points import (
    PickupPointSerializer
)
from .telegram_users import TelegramUserSerializer
from .users import UserSerializer

__all__ = [
    # Auth (Сессии, пароли, коды)
    "EmailPasswordTokenObtainPairSerializer",
    "ChangePasswordSerializer",
    "EmailSerializer",
    "VerifyCodeSerializer",
    "ResetPasswordSerializer",
    "VerifyTokenSerializer",
    
    # Users & TG
    "UserSerializer",
    "TelegramUserSerializer",
    
    # Orders
    "OrderListSerializer",
    "OrderDetailSerializer",
    "OrderCreateSerializer",
    
    # ПВЗ & Маркетплейсы
    "PickupPointSerializer",
    "PickupPointListSerializer",
    "PickupPointDetailSerializer",
    "MarketplaceSerializer",
    
    # Инструменты
    "NewsletterSerializer",
]
