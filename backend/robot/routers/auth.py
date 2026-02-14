"""
robot/routers/auth.py

Все auth endpoints в одном месте
"""
from django.urls import path

from ..views import (
    EmailPasswordLoginView,
    UsernamePasswordLoginView,
    RefreshTokenView,
    LogoutView,
    CurrentUserView,
    VerifyTokenView,
)

# Твои auth endpoints
auth_urls = [
    path('login/email/', EmailPasswordLoginView.as_view(), name='email-login'),
    path('login/username/', UsernamePasswordLoginView.as_view(), name='username-login'),
    path('refresh/', RefreshTokenView.as_view(), name='refresh-token'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('me/', CurrentUserView.as_view(), name='current-user'),
    path('verify/', VerifyTokenView.as_view(), name='verify-token'),
]

__all__ = ['auth_urls']
