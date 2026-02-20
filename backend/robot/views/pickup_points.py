from drf_spectacular.utils import extend_schema_view
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from ..models import PickupPoint
from ..schemas.pickup_points import (pickup_points_by_marketplace_schema,
                                     pickup_points_create_schema,
                                     pickup_points_destroy_schema,
                                     pickup_points_list_schema,
                                     pickup_points_retrieve_schema,
                                     pickup_points_update_schema)
from ..serializers import PickupPointSerializer


@extend_schema_view(
    list=pickup_points_list_schema,
    create=pickup_points_create_schema,
    retrieve=pickup_points_retrieve_schema,
    update=pickup_points_update_schema,
    partial_update=pickup_points_update_schema,  # ← PATCH /{id}/ тоже под PickupPoints
    destroy=pickup_points_destroy_schema,
    by_marketplace=pickup_points_by_marketplace_schema,
)
class PickupPointViewSet(viewsets.ModelViewSet):
    queryset = PickupPoint.objects.all()
    serializer_class = PickupPointSerializer
    permission_classes = (IsAuthenticated,)

    @action(detail=False, methods=["get"])
    def by_marketplace(self, request):
        marketplace = request.query_params.get("marketplace")

        if not marketplace:
            return Response(
                {"error": "marketplace параметр обязателен"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        pickup_points = PickupPoint.objects.filter(marketplace=marketplace)
        serializer = self.get_serializer(pickup_points, many=True)
        return Response(serializer.data)
