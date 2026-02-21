from rest_framework import serializers

from ..models import Marketplace, PickupPoint, TelegramUser
from .telegram_users import TelegramUserSerializer


class MarketplaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Marketplace
        fields = ("id", "code", "name")


class PickupPointSerializer(serializers.ModelSerializer):
    admin_telegram_user = TelegramUserSerializer(read_only=True)
    admin_telegram_user_id = serializers.IntegerField(write_only=True)

    marketplaces = MarketplaceSerializer(many=True, read_only=True)
    marketplace_ids = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True,
        required=False,
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

    def validate_admin_telegram_user_id(self, value):
        if not TelegramUser.objects.filter(id=value).exists():
            raise serializers.ValidationError("Telegram пользователь не найден")
        return value

    def validate_marketplace_ids(self, value):
        qs = Marketplace.objects.filter(id__in=value)
        if qs.count() != len(value):
            raise serializers.ValidationError(
                "Один или несколько маркетплейсов не найдены"
            )
        return value

    def validate_address(self, value):
        if len(value.strip()) < 5:
            raise serializers.ValidationError("Адрес должен быть не менее 5 символов")
        return value

    def create(self, validated_data):
        admin_id = validated_data.pop("admin_telegram_user_id")
        marketplace_ids = validated_data.pop("marketplace_ids", [])

        admin = TelegramUser.objects.get(id=admin_id)
        pickup_point = PickupPoint.objects.create(
            admin_telegram_user=admin, **validated_data
        )

        if marketplace_ids:
            pickup_point.marketplaces.set(
                Marketplace.objects.filter(id__in=marketplace_ids)
            )

        return pickup_point

    def update(self, instance, validated_data):
        admin_id = validated_data.pop("admin_telegram_user_id", None)
        marketplace_ids = validated_data.pop("marketplace_ids", None)

        if admin_id:
            instance.admin_telegram_user = TelegramUser.objects.get(id=admin_id)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()

        if marketplace_ids is not None:
            instance.marketplaces.set(
                Marketplace.objects.filter(id__in=marketplace_ids)
            )

        return instance


class PickupPointListSerializer(serializers.ModelSerializer):
    marketplaces = MarketplaceSerializer(many=True, read_only=True)

    class Meta:
        model = PickupPoint
        fields = ("id", "address", "marketplaces")
        read_only_fields = ("id",)


class PickupPointDetailSerializer(serializers.ModelSerializer):
    admin_telegram_user = TelegramUserSerializer(read_only=True)
    marketplaces = MarketplaceSerializer(many=True, read_only=True)

    class Meta:
        model = PickupPoint
        fields = (
            "id",
            "address",
            "marketplaces",
            "admin_telegram_user",
        )
        read_only_fields = ("id",)
