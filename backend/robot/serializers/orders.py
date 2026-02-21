# robot/serializers/orders.py

from rest_framework import serializers

from ..models import Marketplace, Order, PickupPoint
from .pickup_points import PickupPointSerializer
from .users import UserSerializer


class OrderListSerializer(serializers.ModelSerializer):
    customer = UserSerializer(read_only=True)
    pickup_point = PickupPointSerializer(read_only=True)
    status_display = serializers.CharField(source="get_status_display", read_only=True)

    class Meta:
        model = Order
        fields = (
            "id",
            "customer",
            "pickup_point",
            "full_name",
            "amount",
            "status",
            "status_display",
            "date_created",
        )
        read_only_fields = ("id", "date_created")


class OrderDetailSerializer(serializers.ModelSerializer):
    customer = UserSerializer(read_only=True)
    pickup_point = PickupPointSerializer(read_only=True)
    status_display = serializers.CharField(source="get_status_display", read_only=True)

    class Meta:
        model = Order
        fields = (
            "id",
            "customer",
            "pickup_point",
            "full_name",
            "amount",
            "comment",
            "barcode_image",
            "status",
            "status_display",
            "date_created",
        )
        read_only_fields = ("id", "date_created")


class OrderCreateSerializer(serializers.ModelSerializer):
    pickup_point_id = serializers.IntegerField(write_only=True)
    marketplace_id = serializers.IntegerField(write_only=True)
    customer_id = serializers.IntegerField(write_only=True, required=False)  # для бота

    class Meta:
        model = Order
        fields = (
            "id",
            "full_name",
            "amount",
            "comment",
            "barcode_image",
            "pickup_point_id",
            "marketplace_id",
            "customer_id",
        )

    def validate_pickup_point_id(self, value):
        if not PickupPoint.objects.filter(id=value).exists():
            raise serializers.ValidationError("Пункт выдачи не найден")
        return value

    def validate_marketplace_id(self, value):
        if not Marketplace.objects.filter(id=value).exists():
            raise serializers.ValidationError("Маркетплейс не найден")
        return value

    def validate_amount(self, value):
        try:
            float(value)
        except (ValueError, TypeError):
            raise serializers.ValidationError("Сумма должна быть числом")
        return value

    def create(self, validated_data):
        customer_id = validated_data.pop("customer_id", None)
        if customer_id:
            # если передан ботом — используем AppUser по ID
            from django.contrib.auth import get_user_model

            AppUser = get_user_model()
            customer = AppUser.objects.get(id=customer_id)
        else:
            # иначе берем request.user как раньше
            customer = self.context["request"].user

        pickup_point_id = validated_data.pop("pickup_point_id")
        pickup_point = PickupPoint.objects.get(id=pickup_point_id)

        marketplace_id = validated_data.pop("marketplace_id")
        marketplace = Marketplace.objects.get(id=marketplace_id)

        if not pickup_point.marketplaces.filter(id=marketplace.id).exists():
            raise serializers.ValidationError(
                "Выбранный маркетплейс недоступен для этого ПВЗ"
            )

        order = Order.objects.create(
            customer=customer,
            pickup_point=pickup_point,
            marketplace=marketplace,
            **validated_data,
        )
        return order
