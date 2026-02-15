from rest_framework import serializers

from ..models import TelegramUser


class TelegramUserSerializer(serializers.ModelSerializer):
    email = serializers.SerializerMethodField()
    phone_number = serializers.SerializerMethodField()
    app_user = serializers.SerializerMethodField()

    class Meta:
        model = TelegramUser
        fields = (
            "id",
            "app_user",
            "user_id",
            "name",
            "nick_name",
            "email",
            "phone_number",
            "is_blocked",
            "is_administrator",
            "date_join",
        )
        read_only_fields = ("id", "date_join")

    def get_email(self, obj):
        return obj.app_user.email if obj.app_user else None

    def get_phone_number(self, obj):
        return obj.app_user.phone_number if obj.app_user else None

    def get_app_user(self, obj):
        return obj.app_user.id if obj.app_user else None
