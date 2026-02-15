from rest_framework import serializers

from ..models import AppUser, TelegramUser


class TelegramUserSerializer(serializers.ModelSerializer):
    email = serializers.SerializerMethodField(read_only=True)
    phone_number = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = TelegramUser
        fields = (
            "id",
            "user_id",
            "name",
            "nick_name",
            "email",
            "phone_number",
            "is_blocked",
            "is_administrator",
            "date_join",
        )
        read_only_fields = ("id", "date_join", "email", "phone_number")

    def get_email(self, obj):
        return obj.app_user.email if obj.app_user else None

    def get_phone_number(self, obj):
        return obj.app_user.phone_number if obj.app_user else None


class TelegramUserListSerializer(serializers.ModelSerializer):
    app_user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = TelegramUser
        fields = (
            "id",
            "user_id",
            "name",
            "nick_name",
            "is_blocked",
            "date_join",
            "app_user",
        )
        read_only_fields = ("id", "date_join")


class TelegramUserDetailSerializer(serializers.ModelSerializer):
    app_user = serializers.StringRelatedField(read_only=True)
    email = serializers.SerializerMethodField(read_only=True)
    phone_number = serializers.SerializerMethodField(read_only=True)

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
            "email",
            "phone_number",
        )
        read_only_fields = ("id", "date_join", "email", "phone_number")

    def get_email(self, obj):
        return obj.app_user.email if obj.app_user else None

    def get_phone_number(self, obj):
        return obj.app_user.phone_number if obj.app_user else None
