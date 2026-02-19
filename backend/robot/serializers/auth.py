"""
robot/serializers/auth.py

Сериализаторы для аутентификации и управления пользователями
"""

from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

AppUser = get_user_model()


class EmailPasswordTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = "email"  # ключевой момент

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")
        if not email or not password:
            raise serializers.ValidationError("Email и пароль обязательны")

        user = AppUser.objects.filter(email=email).first()
        if user is None or not user.check_password(password):
            raise serializers.ValidationError("Неверный email или пароль")

        # теперь вызываем базовый метод с правильным username_field
        data = super().validate({"email": email, "password": password})
        data["status"] = "success"
        return data
