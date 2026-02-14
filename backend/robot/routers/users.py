"""
robot/routers/users.py

Все endpoints для работы с пользователями
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from ..views import UserViewSet

router = DefaultRouter()
router.register(r'', UserViewSet, basename='user')

users_urls = [
    path('', include(router.urls)),
]

__all__ = ['users_urls']
