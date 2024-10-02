from rest_framework import viewsets
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from robot.models import *

from .filters import *
from .serializer import *


class TelegramUserViewSet(viewsets.ModelViewSet):
    serializer_class = TelegramUserSerializer
    queryset = TelegramUser.objects.all().order_by("id")
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    filterset_class = TelegramUserFilter


class PickupPointViewSet(viewsets.ModelViewSet):
    serializer_class = PickupPointSerializer
    queryset = PickupPoint.objects.all().order_by("id")
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    filterset_class = PickupPointFilter


class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    queryset = Order.objects.all().order_by("id")
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    filterset_class = OrderFilter
