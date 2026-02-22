from rest_framework import serializers
from ..models import Order, PickupPoint, Marketplace
from .users import UserSerializer
from .pickup_points import PickupPointSerializer

# === 1. Сериализатор для СПИСКА ===
class OrderListSerializer(serializers.ModelSerializer):
    customer = UserSerializer(read_only=True)
    pickup_point = PickupPointSerializer(read_only=True)
    status_display = serializers.CharField(source="get_status_display", read_only=True)

    class Meta:
        model = Order
        fields = (
            "id", "customer", "pickup_point", "full_name", 
            "amount", "status", "status_display", "date_created"
        )
        read_only_fields = ("id", "date_created")

# === 2. Сериализатор для ДЕТАЛЕЙ ===
class OrderDetailSerializer(serializers.ModelSerializer):
    customer = UserSerializer(read_only=True)
    pickup_point = PickupPointSerializer(read_only=True)
    status_display = serializers.CharField(source="get_status_display", read_only=True)

    class Meta:
        model = Order
        fields = (
            "id", "customer", "pickup_point", "full_name", 
            "amount", "comment", "barcode_image", "status", 
            "status_display", "date_created"
        )
        read_only_fields = ("id", "date_created")

# === 3. Сериализатор для СОЗДАНИЯ ===
class OrderCreateSerializer(serializers.ModelSerializer):
    pickup_point = serializers.PrimaryKeyRelatedField(
        queryset=PickupPoint.objects.all()
    )
    marketplace = serializers.PrimaryKeyRelatedField(
        queryset=Marketplace.objects.all()
    )
    customer_id = serializers.IntegerField(write_only=True, required=False)

    class Meta:
        model = Order
        fields = (
            "id", "full_name", "amount", "comment", 
            "barcode_image", "pickup_point", "marketplace", "customer_id"
        )

    def validate(self, attrs):
        pickup_point = attrs.get('pickup_point')
        marketplace = attrs.get('marketplace')
        if not pickup_point.marketplaces.filter(id=marketplace.id).exists():
            raise serializers.ValidationError(
                {"marketplace": "Выбранный маркетплейс недоступен для этого ПВЗ"}
            )
        return attrs

    def create(self, validated_data):
        customer_id = validated_data.pop("customer_id", None)
        if customer_id:
            from django.contrib.auth import get_user_model
            customer = get_user_model().objects.get(id=customer_id)
        else:
            customer = self.context["request"].user
        
        return Order.objects.create(customer=customer, **validated_data)
