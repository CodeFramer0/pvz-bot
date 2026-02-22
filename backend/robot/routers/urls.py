from django.urls import include, path
from rest_framework.routers import DefaultRouter
from ..views import MarketPlaceViewSet, NewsletterAPIView, OrderViewSet, TelegramUserViewSet,UserViewSet,PickupPointViewSet

router = DefaultRouter()
# Теперь здесь CRUD + /me/ + /change-password/
router.register(r"users", UserViewSet, basename="user")
router.register(r"telegram-users", TelegramUserViewSet, basename="telegram-user")
router.register(r"orders", OrderViewSet, basename="order")
router.register(r"marketplaces", MarketPlaceViewSet, basename="marketplace")
router.register(r"pickup-points",PickupPointViewSet,basename="pickup-point")
urlpatterns = [
    path("", include(router.urls)),
    
    # Подключаем наш новый конфиг auth
    path("auth/", include("robot.routers.auth")),
    
    path("newsletter/", NewsletterAPIView.as_view(), name="newsletter"),
]
