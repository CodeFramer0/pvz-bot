# robot/serializers/orders.py

from rest_framework import serializers

from ..models import Order, PickupPoint
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

    class Meta:
        model = Order
        fields = (
            "full_name",
            "amount",
            "comment",
            "barcode_image",
            "pickup_point_id",
        )

    def validate_pickup_point_id(self, value):
        if not PickupPoint.objects.filter(id=value).exists():
            raise serializers.ValidationError("Пункт выдачи не найден")
        return value

    def validate_amount(self, value):
        try:
            float(value)
        except (ValueError, TypeError):
            raise serializers.ValidationError("Сумма должна быть числом")
        return value

    def create(self, validated_data):
        request = self.context["request"]

        pickup_point_id = validated_data.pop("pickup_point_id")
        pickup_point = PickupPoint.objects.get(id=pickup_point_id)

        order = Order.objects.create(
            customer=request.user,   # берём из JWT
            pickup_point=pickup_point,
            **validated_data,
        )

        return order
