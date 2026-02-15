"""
robot/serializers/users.py

Сериализаторы для пользователей приложения
"""

from django.contrib.auth import get_user_model
from rest_framework import serializers

AppUser = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """Основной сериализатор пользователя"""

    class Meta:
        model = AppUser
        fields = (
            "id",
            "username",
            "email",
            "phone_number",
            "first_name",
            "last_name",
            "is_active",
            "date_joined",
        )
        read_only_fields = ("id", "date_joined")
