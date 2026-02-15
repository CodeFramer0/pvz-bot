"""
robot/views/__init__.py

Главный файл, который импортирует все views из отдельных модулей
"""

from .auth import (ChangePasswordView, CurrentUserView, EmailPasswordLoginView,
                   LogoutView, RefreshTokenView, SendVerificationCodeView,
                   UsernamePasswordLoginView, VerifyCodeView, VerifyTokenView)
from .orders import OrderViewSet
from .pickup_points import PickupPointViewSet
from .telegram_users import TelegramUserViewSet
from .users import UserViewSet

__all__ = [
    # Auth Views
    "EmailPasswordLoginView",
    "UsernamePasswordLoginView",
    "RefreshTokenView",
    "LogoutView",
    "CurrentUserView",
    "ChangePasswordView",
    "VerifyTokenView",
    "VerifyCodeView",
    "SendVerificationCodeView",
    # ViewSets
    "OrderViewSet",
    "PickupPointViewSet",
    "UserViewSet",
    "TelegramUserViewSet",
]
