from .auth import (
    EmailTokenObtainPairView, 
    RefreshTokenView,
    LogoutView,
    ResetPasswordView, 
    SendVerificationCodeView, 
    VerifyCodeView,
    VerifyTokenView
)
from .marketplace import MarketPlaceViewSet
from .news_letter import NewsletterAPIView
from .orders import OrderViewSet
from .pickup_points import PickupPointViewSet
from .telegram_users import TelegramUserViewSet
from .users import UserViewSet

__all__ = [
    # Auth & Session (из auth.py)
    "EmailTokenObtainPairView",
    "RefreshTokenView",
    "LogoutView",
    "SendVerificationCodeView",
    "VerifyCodeView",
    "ResetPasswordView",
    "VerifyTokenView",
    
    # ViewSets (CRUD + Actions)
    "UserViewSet",          # Теперь включает /me/ и /change-password/
    "OrderViewSet",
    "MarketPlaceViewSet",
    "PickupPointViewSet",
    "TelegramUserViewSet",
    
    # APIViews
    "NewsletterAPIView",
]
