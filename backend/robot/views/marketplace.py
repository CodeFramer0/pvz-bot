from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated

from ..models import Marketplace
from ..serializers import MarketplaceSerializer

@extend_schema_view(
    list=extend_schema(
        summary="Список маркетплейсов",
        description="Получение списка всех доступных торговых площадок.",
        tags=["Marketplaces"]
    ),
    retrieve=extend_schema(
        summary="Детальная информация о маркетплейсе",
        description="Получение данных конкретного маркетплейса по ID.",
        tags=["Marketplaces"]
    ),
    create=extend_schema(
        summary="Создать маркетплейс",
        description="Добавление новой площадки в систему.",
        tags=["Marketplaces"]
    ),
    update=extend_schema(
        summary="Обновить маркетплейс",
        description="Полное обновление данных площадки.",
        tags=["Marketplaces"]
    ),
    partial_update=extend_schema(
        summary="Изменить маркетплейс",
        description="Частичное редактирование полей площадки.",
        tags=["Marketplaces"]
    ),
    destroy=extend_schema(
        summary="Удалить маркетплейс",
        description="Удаление площадки из базы данных.",
        tags=["Marketplaces"]
    ),
)
class MarketPlaceViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Marketplace.objects.all()
    serializer_class = MarketplaceSerializer
