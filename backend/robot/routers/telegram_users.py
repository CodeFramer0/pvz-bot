"""
robot/routers/telegram_users.py

Все endpoints для работы с Telegram пользователями
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from ..views import TelegramUserViewSet

router = DefaultRouter()
router.register(r'', TelegramUserViewSet, basename='telegram-user')

telegram_users_urls = [
    path('', include(router.urls)),
]

__all__ = ['telegram_users_urls']
