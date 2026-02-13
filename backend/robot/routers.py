from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from .views import *

router = DefaultRouter()
router.register(r"auth", AuthViewSet, basename="auth")
router.register(r"users", AppUserViewSet, basename="users")
router.register(r"telegram-users", TelegramUserViewSet, basename="telegram-users")
router.register(r"pickup-points", PickupPointViewSet, basename="pickup-points")
router.register(r"orders", OrderViewSet, basename="orders")


urlpatterns = [
    path("", include(router.urls)),
    path("auth/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
