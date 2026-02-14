from django.urls import path, include

from .auth import auth_urls
from .orders import orders_urls
from .pickup_points import pickup_points_urls
from .users import users_urls
from .telegram_users import telegram_users_urls

urlpatterns = [
    path('auth/', include(auth_urls)),
    path('users/', include(users_urls)),
    path('orders/', include(orders_urls)),
    path('pickup-points/', include(pickup_points_urls)),
    path('telegram-users/', include(telegram_users_urls)),
]

__all__ = ['urlpatterns']