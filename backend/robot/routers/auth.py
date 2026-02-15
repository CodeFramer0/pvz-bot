"""
robot/routers/auth.py

Все auth endpoints в одном месте
"""

from django.urls import path

from ..views import (CurrentUserView, EmailPasswordLoginView, LogoutView,
                     RefreshTokenView, SendVerificationCodeView,
                     UsernamePasswordLoginView, VerifyCodeView,
                     VerifyTokenView)

# Все auth endpoints
urlpatterns = [
    path("login/email/", EmailPasswordLoginView.as_view(), name="email-login"),
    path("login/username/", UsernamePasswordLoginView.as_view(), name="username-login"),
    path("refresh/", RefreshTokenView.as_view(), name="refresh-token"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("me/", CurrentUserView.as_view(), name="current-user"),
    path("verify/", VerifyTokenView.as_view(), name="verify-token"),
    path(
        "verify/send-code/",
        SendVerificationCodeView.as_view(),
        name="send-verification-code",
    ),
    path("verify/confirm/", VerifyCodeView.as_view(), name="verify-code"),
]

__all__ = ["urlpatterns"]
