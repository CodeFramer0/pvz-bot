from django.urls import path
from ..views.auth import (
    EmailTokenObtainPairView, RefreshTokenView, LogoutView,
    SendVerificationCodeView, VerifyCodeView, ResetPasswordView, VerifyTokenView
)

urlpatterns = [
    # JWT сессии
    path("login/", EmailTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("refresh/", RefreshTokenView.as_view(), name="token_refresh"),
    path("logout/", LogoutView.as_view(), name="logout"),
    
    # Восстановление пароля (Redis Flow)
    path("password-reset/send-code/", SendVerificationCodeView.as_view(), name="password_reset_send"),
    path("password-reset/verify-code/", VerifyCodeView.as_view(), name="password_reset_verify"),
    path("password-reset/confirm/", ResetPasswordView.as_view(), name="password_reset_confirm"),
    
    # Утилиты
    path("verify-token/", VerifyTokenView.as_view(), name="token_verify"),
]
