from django_filters import rest_framework as rest_framework_filters
from robot.models import *


class TelegramUserFilter(rest_framework_filters.FilterSet):
    user_id = rest_framework_filters.CharFilter(
        field_name="user_id", lookup_expr="exact"
    )

    class Meta:
        model = TelegramUser
        fields = ["user_id"]


class PickupPointFilter(rest_framework_filters.FilterSet):
    address = rest_framework_filters.CharFilter(
        field_name="address", lookup_expr="icontains"
    )
    marketplace = rest_framework_filters.CharFilter(
        field_name="marketplace", lookup_expr="exact"
    )

    class Meta:
        model = PickupPoint
        fields = ["address", "marketplace"]


class OrderFilter(rest_framework_filters.FilterSet):
    customer = rest_framework_filters.CharFilter(
        field_name="customer__user_id", lookup_expr="exact"
    )
    status = rest_framework_filters.CharFilter(field_name="status", lookup_expr="exact")
    pickup_point = rest_framework_filters.CharFilter(
        field_name="pickup_point__address", lookup_expr="icontains"
    )

    class Meta:
        model = Order
        fields = ["customer", "status", "pickup_point"]
