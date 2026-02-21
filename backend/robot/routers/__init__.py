from django.urls import include, path
from rest_framework.routers import DefaultRouter

from ..views import (MarketPlaceViewSet, OrderViewSet, TelegramUserViewSet,
                     UserViewSet)

# добавь другие ViewSet-и по аналогии

router = DefaultRouter()
router.register(r"users", UserViewSet, basename="user")
router.register(r"telegram-users", TelegramUserViewSet, basename="telegram-user")
router.register(r"orders", OrderViewSet, basename="order")
router.register(r"marketplaces", MarketPlaceViewSet, basename="marketplace")
# и так далее для других роутов

urlpatterns = [
    path("", include(router.urls)),
    path("auth/", include("robot.routers.auth")),
    path("users/", include("robot.routers.users")),
    path("orders/", include("robot.routers.orders")),
    path("marketplaces/", include("robot.routers.marketplaces")),
    path("pickup-points/", include("robot.routers.pickup_points")),
    path("telegram-users/", include("robot.routers.telegram_users")),
]
