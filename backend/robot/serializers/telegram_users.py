from rest_framework import serializers
from ..models import TelegramUser

class TelegramUserSerializer(serializers.ModelSerializer):
    # Используем source='app_user.field'. 
    # allow_null=True позволяет не падать, если app_user отсутствует (null)
    email = serializers.EmailField(source="app_user.email", read_only=True, allow_null=True)
    phone_number = serializers.CharField(source="app_user.phone_number", read_only=True, allow_null=True)
    app_user_id = serializers.IntegerField(source="app_user.id", read_only=True, allow_null=True)

    class Meta:
        model = TelegramUser
        fields = (
            "id",
            "app_user_id",
            "user_id",
            "name",
            "nick_name",
            "email",
            "phone_number",
            "is_blocked",
            "is_administrator",
            "date_join",
        )
        read_only_fields = ("id", "date_join", "user_id")

    # Методы get_email, get_phone_number и get_app_user больше не нужны
