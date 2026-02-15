"""
robot/routers/telegram_users.py

Все endpoints для работы с Telegram пользователями
"""

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from ..views import TelegramUserViewSet

router = DefaultRouter()
router.register(r"", TelegramUserViewSet, basename="telegram-user")

urlpatterns = [
    path("", include(router.urls)),
]

__all__ = ["urlpatterns"]
