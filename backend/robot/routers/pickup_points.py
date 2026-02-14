"""
robot/routers/pickup_points.py

Все endpoints для работы с пунктами выдачи
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from ..views import PickupPointViewSet

router = DefaultRouter()
router.register(r'', PickupPointViewSet, basename='pickup-point')

pickup_points_urls = [
    path('', include(router.urls)),
]

__all__ = ['pickup_points_urls']
