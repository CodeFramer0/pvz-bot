from rest_framework import serializers
from ..models import Marketplace

class MarketplaceSerializer(serializers.ModelSerializer):
    """
    Сериализатор для работы с торговыми площадками.
    """
    class Meta:
        model = Marketplace
        fields = ("id", "code", "name")
        read_only_fields = ("id",)

    def validate_code(self, value):
        """Приводим код к верхнему регистру для единообразия (например, WB, OZON)"""
        return value.upper()
