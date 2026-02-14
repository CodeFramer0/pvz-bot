"""
robot/serializers/pickup_points.py

Сериализаторы для пунктов выдачи
"""
from rest_framework import serializers
from ..models import PickupPoint, TelegramUser
from .telegram_users import TelegramUserSerializer


class PickupPointSerializer(serializers.ModelSerializer):
    """Основной сериализатор пункта выдачи"""
    admin_telegram_user = TelegramUserSerializer(read_only=True)
    admin_telegram_user_id = serializers.IntegerField(write_only=True)
    marketplace_display = serializers.CharField(source='get_marketplace_display', read_only=True)

    class Meta:
        model = PickupPoint
        fields = ('id', 'address', 'marketplace', 'marketplace_display', 
                  'admin_telegram_user', 'admin_telegram_user_id')
        read_only_fields = ('id',)

    def validate_admin_telegram_user_id(self, value):
        if not TelegramUser.objects.filter(id=value).exists():
            raise serializers.ValidationError("Telegram пользователь не найден")
        return value

    def validate_address(self, value):
        if len(value.strip()) < 5:
            raise serializers.ValidationError("Адрес должен быть не менее 5 символов")
        return value

    def create(self, validated_data):
        admin_id = validated_data.pop('admin_telegram_user_id')
        admin = TelegramUser.objects.get(id=admin_id)
        pickup_point = PickupPoint.objects.create(
            admin_telegram_user=admin,
            **validated_data
        )
        return pickup_point

    def update(self, instance, validated_data):
        admin_id = validated_data.pop('admin_telegram_user_id', None)
        if admin_id:
            instance.admin_telegram_user = TelegramUser.objects.get(id=admin_id)
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class PickupPointListSerializer(serializers.ModelSerializer):
    """Сериализатор пункта выдачи (список)"""
    marketplace_display = serializers.CharField(source='get_marketplace_display', read_only=True)

    class Meta:
        model = PickupPoint
        fields = ('id', 'address', 'marketplace', 'marketplace_display')
        read_only_fields = ('id',)


class PickupPointDetailSerializer(serializers.ModelSerializer):
    """Сериализатор пункта выдачи (детали)"""
    admin_telegram_user = TelegramUserSerializer(read_only=True)
    marketplace_display = serializers.CharField(source='get_marketplace_display', read_only=True)

    class Meta:
        model = PickupPoint
        fields = ('id', 'address', 'marketplace', 'marketplace_display', 'admin_telegram_user')
        read_only_fields = ('id',)
