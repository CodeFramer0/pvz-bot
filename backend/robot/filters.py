from django_filters import rest_framework as filters

from .models import Order, PickupPoint, TelegramUser


class TelegramUserFilter(filters.FilterSet):
    nick_name = filters.CharFilter(field_name="nick_name", lookup_expr="icontains")
    is_administrator = filters.BooleanFilter()
    is_blocked = filters.BooleanFilter()
    user_id = filters.NumberFilter(field_name="user_id", lookup_expr="exact")

    class Meta:
        model = TelegramUser
        fields = ["nick_name", "is_administrator", "is_blocked"]


class OrderFilter(filters.FilterSet):
    status = filters.ChoiceFilter(choices=Order.STATUS_CHOICES)
    date_created = filters.DateFromToRangeFilter()
    full_name = filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = Order
        fields = ["status", "date_created", "full_name", "pickup_point"]


class PickupPointFilter(filters.FilterSet):
    marketplace = filters.ChoiceFilter(choices=PickupPoint.MARKETPLACE_CHOICES)
    address = filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = PickupPoint
        fields = ["marketplace", "address"]
