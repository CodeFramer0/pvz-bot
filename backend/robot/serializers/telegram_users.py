from rest_framework import serializers
from ..models import TelegramUser, AppUser


class TelegramUserSerializer(serializers.ModelSerializer):
    """Сериализатор для создания/обновления Telegram пользователя"""
    class Meta:
        model = TelegramUser
        fields = (
            "id",
            "user_id",
            "name",
            "nick_name",
            "is_blocked",
            "is_administrator",
            "date_join",
            "app_user",
        )
        read_only_fields = ("id", "date_join")

    def validate_user_id(self, value):
        if self.instance is None and TelegramUser.objects.filter(user_id=value).exists():
            raise serializers.ValidationError("Пользователь с таким Telegram ID уже существует")
        return value

    def validate_app_user(self, value):
        if value and not AppUser.objects.filter(id=value.id).exists():
            raise serializers.ValidationError("Привязанный AppUser не найден")
        return value


class TelegramUserListSerializer(serializers.ModelSerializer):
    """Список Telegram пользователей"""
    class Meta:
        model = TelegramUser
        fields = ("id", "user_id", "name", "nick_name", "is_blocked", "date_join")
        read_only_fields = ("id", "date_join")


class TelegramUserDetailSerializer(serializers.ModelSerializer):
    """Детали Telegram пользователя"""
    app_user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = TelegramUser
        fields = (
            "id",
            "user_id",
            "name",
            "nick_name",
            "is_blocked",
            "is_administrator",
            "date_join",
            "app_user",
        )
        read_only_fields = ("id", "date_join")
