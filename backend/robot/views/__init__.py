"""
robot/views/__init__.py

Главный файл, который импортирует все views из отдельных модулей
"""
from .auth import (
    EmailPasswordLoginView,
    UsernamePasswordLoginView,
    RefreshTokenView,
    LogoutView,
    CurrentUserView,
    ChangePasswordView,
    VerifyTokenView,
)

from .orders import OrderViewSet
from .pickup_points import PickupPointViewSet
from .users import UserViewSet
from .telegram_users import TelegramUserViewSet

__all__ = [
    # Auth Views
    'EmailPasswordLoginView',
    'UsernamePasswordLoginView',
    'RefreshTokenView',
    'LogoutView',
    'CurrentUserView',
    'ChangePasswordView',
    'VerifyTokenView',
    
    # ViewSets
    'OrderViewSet',
    'PickupPointViewSet',
    'UserViewSet',
    'TelegramUserViewSet',
]
