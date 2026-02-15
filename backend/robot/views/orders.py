from drf_spectacular.utils import extend_schema_view
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from ..models import Order
from ..schemas.orders import (orders_create_schema, orders_destroy_schema,
                              orders_list_schema, orders_retrieve_schema,
                              orders_update_schema,
                              orders_update_status_schema)
from ..serializers import (OrderCreateSerializer, OrderDetailSerializer,
                           OrderListSerializer)
from rest_framework.parsers import MultiPartParser, FormParser

@extend_schema_view(
    list=orders_list_schema,
    create=orders_create_schema,
    retrieve=orders_retrieve_schema,
    update=orders_update_schema,
    partial_update=orders_update_schema,  # ← PATCH /{id}/ попадёт в Orders
    destroy=orders_destroy_schema,
    update_status=orders_update_status_schema,
)
class OrderViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    parser_classes = [MultiPartParser, FormParser]
    queryset = Order.objects.all().order_by("-date_created")
    def get_serializer_class(self):
        if self.action == "retrieve":
            return OrderDetailSerializer
        elif self.action == "create":
            return OrderCreateSerializer
        return OrderListSerializer

    @action(detail=True, methods=["patch"])
    def update_status(self, request, pk=None):
        order = self.get_object()
        new_status = request.data.get("status")

        if new_status not in dict(Order.STATUS_CHOICES):
            return Response(
                {"error": "Неверный статус"}, status=status.HTTP_400_BAD_REQUEST
            )

        order.status = new_status
        order.save()

        return Response(OrderDetailSerializer(order).data, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=["get"], url_path="my_orders")
    def my_orders(self, request):
        """
        Возвращает все заказы текущего пользователя
        """
        orders = Order.objects.filter(customer=self.request.user).order_by("-date_created")
        serializer = self.get_serializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)