from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from ..models import PickupPoint
from ..serializers import PickupPointSerializer

@extend_schema_view(
    list=extend_schema(summary="Список всех ПВЗ", tags=["Pickup Points"]),
    retrieve=extend_schema(summary="Информация о конкретном ПВЗ", tags=["Pickup Points"]),
    create=extend_schema(summary="Добавить новый ПВЗ", tags=["Pickup Points"]),
    update=extend_schema(summary="Обновить данные ПВЗ", tags=["Pickup Points"]),
    partial_update=extend_schema(summary="Изменить данные ПВЗ", tags=["Pickup Points"]),
    destroy=extend_schema(summary="Удалить ПВЗ", tags=["Pickup Points"]),
)
class PickupPointViewSet(viewsets.ModelViewSet):
    queryset = PickupPoint.objects.all()
    serializer_class = PickupPointSerializer
    permission_classes = (IsAuthenticated,)

    @extend_schema(
        summary="Фильтрация ПВЗ по маркетплейсу",
        description="Возвращает список пунктов выдачи для конкретной площадки (например, 'Wildberries' или 'Ozon').",
        parameters=[
            OpenApiParameter(
                name="marketplace",
                description="ID или слаг маркетплейса",
                required=True,
                type=str
            ),
        ],
        responses={200: PickupPointSerializer(many=True)},
        tags=["Pickup Points"]
    )
    @action(detail=False, methods=["get"], url_path="by-marketplace")
    def by_marketplace(self, request):
        marketplace = request.query_params.get("marketplace")

        if not marketplace:
            return Response(
                {"error": "Параметр 'marketplace' обязателен"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        pickup_points = PickupPoint.objects.filter(marketplace=marketplace)
        serializer = self.get_serializer(pickup_points, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
