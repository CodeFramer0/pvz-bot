from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

AppUser = get_user_model()

# === JWT Login ===

class EmailPasswordTokenObtainPairSerializer(TokenObtainPairSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].help_text = "Введите логин или Email"

# === Password change ===
class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True, min_length=8)
    new_password_confirm = serializers.CharField(write_only=True)

    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password_confirm']:
            raise serializers.ValidationError({"new_password_confirm": "Пароли не совпадают"})
        return attrs

# === Email & Auth flow ===
class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField()

class VerifyCodeSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField(max_length=6, min_length=6)

class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField(help_text="Временный токен, полученный после проверки кода")
    new_password = serializers.CharField(write_only=True, min_length=8)
    new_password_confirm = serializers.CharField(write_only=True)

    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password_confirm']:
            raise serializers.ValidationError({"new_password_confirm": "Пароли не совпадают"})
        return attrs

class VerifyTokenSerializer(serializers.Serializer):
    token = serializers.CharField()

class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField(help_text="Refresh токен для занесения в черный список")
