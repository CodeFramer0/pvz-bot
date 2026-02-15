from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema_view
from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated

from ..schemas.users import (users_create_schema, users_destroy_schema,
                             users_list_schema, users_retrieve_schema,
                             users_update_schema)
from ..serializers import UserSerializer

AppUser = get_user_model()


@extend_schema_view(
    list=users_list_schema,
    create=users_create_schema,
    retrieve=users_retrieve_schema,
    update=users_update_schema,
    partial_update=users_update_schema,  # ← PATCH /users/{id}/ тоже под Users
    destroy=users_destroy_schema,
)
class UserViewSet(viewsets.ModelViewSet):
    queryset = AppUser.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer  # ваш основной сериализатор AppUser
