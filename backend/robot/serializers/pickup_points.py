from rest_framework import serializers
from ..models import Marketplace, PickupPoint, TelegramUser
from .telegram_users import TelegramUserSerializer
from .marketplaces import MarketplaceSerializer

class PickupPointSerializer(serializers.ModelSerializer):
    # Используем PrimaryKeyRelatedField: он сам сделает get() и validate()
    admin_telegram_user = TelegramUserSerializer(read_only=True)
    admin_telegram_user_id = serializers.PrimaryKeyRelatedField(
        queryset=TelegramUser.objects.all(),
        source='admin_telegram_user', # DRF сам подставит объект в это поле
        write_only=True
    )

    # Работа с M2M через PrimaryKeyRelatedField (заменяет ListField + ручной .set())
    marketplaces = MarketplaceSerializer(many=True, read_only=True)
    marketplace_ids = serializers.PrimaryKeyRelatedField(
        queryset=Marketplace.objects.all(),
        source='marketplaces', # Автоматически обновит связь m2m
        many=True,
        write_only=True,
        required=False
    )

    class Meta:
        model = PickupPoint
        fields = (
            "id",
            "address",
            "marketplaces",
            "marketplace_ids",
            "admin_telegram_user",
            "admin_telegram_user_id",
        )
        read_only_fields = ("id",)

    def validate_address(self, value):
        if len(value.strip()) < 5:
            raise serializers.ValidationError("Адрес должен быть не менее 5 символов")
        return value