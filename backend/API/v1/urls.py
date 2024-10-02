from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r"telegram_users", views.TelegramUserViewSet, basename="telegram_users")
router.register(r"pickup_points", views.PickupPointViewSet, basename="pickup_points")
router.register(r"orders", views.OrderViewSet, basename="orders")
urlpatterns = router.urls
