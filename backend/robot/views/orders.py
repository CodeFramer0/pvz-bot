from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from ..models import Order
from ..serializers import (OrderCreateSerializer, OrderDetailSerializer,
                           OrderListSerializer)

@extend_schema_view(
    list=extend_schema(summary="Список всех заказов", tags=["Orders"]),
    retrieve=extend_schema(summary="Детальная информация о заказе", tags=["Orders"]),
    create=extend_schema(summary="Создать новый заказ", tags=["Orders"]),
    update=extend_schema(summary="Полное обновление заказа", tags=["Orders"]),
    partial_update=extend_schema(summary="Частичное обновление заказа", tags=["Orders"]),
    destroy=extend_schema(summary="Удалить заказ", tags=["Orders"]),
)
class OrderViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    parser_classes = [MultiPartParser, FormParser]
    queryset = Order.objects.all().order_by("-date_created")

    def get_serializer_class(self):
        if self.action == "retrieve":
            return OrderDetailSerializer
        elif self.action in ["create", "update", "partial_update"]:
            return OrderCreateSerializer
        return OrderListSerializer

    @extend_schema(
        summary="Обновить статус заказа",
        description="Принимает строку статуса из доступных STATUS_CHOICES",
        request=None, # Если нет отдельного сериализатора, можно описать инлайн
        responses={200: OrderDetailSerializer},
        tags=["Orders: Actions"]
    )
    @action(detail=True, methods=["patch"])
    def update_status(self, request, pk=None):
        order = self.get_object()
        new_status = request.data.get("status")

        if new_status not in dict(Order.STATUS_CHOICES):
            return Response(
                {"error": f"Неверный статус. Доступные: {list(dict(Order.STATUS_CHOICES).keys())}"}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        order.status = new_status
        order.save()

        # Используем сериализатор для деталей после обновления
        return Response(OrderDetailSerializer(order).data, status=status.HTTP_200_OK)

    @extend_schema(
        summary="Мои заказы",
        description="Возвращает список заказов, где заказчиком является текущий пользователь",
        responses={200: OrderListSerializer(many=True)},
        tags=["Orders"]
    )
    @action(detail=False, methods=["get"], url_path="my-orders") # url-path лучше через дефис
    def my_orders(self, request):
        orders = Order.objects.filter(customer=self.request.user).order_by("-date_created")
        # get_serializer автоматически выберет OrderListSerializer согласно логике get_serializer_class
        serializer = self.get_serializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
