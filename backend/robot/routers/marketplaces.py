from django.urls import include, path
from rest_framework.routers import DefaultRouter

from ..views import MarketPlaceViewSet

router = DefaultRouter()
router.register(r"", MarketPlaceViewSet, basename="marketplace")  # ← убрали 'MarketPlaces'

urlpatterns = [
    path("", include(router.urls)),
]
