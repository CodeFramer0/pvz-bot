from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from ..models import AppUser
from ..serializers import ChangePasswordSerializer,UserSerializer

@extend_schema_view(
    list=extend_schema(summary="Список пользователей", tags=["Users"]),
    retrieve=extend_schema(summary="Детальная информация о пользователе", tags=["Users"]),
    create=extend_schema(summary="Создать нового пользователя", tags=["Users"]),
    update=extend_schema(summary="Полное обновление пользователя", tags=["Users"]),
    partial_update=extend_schema(summary="Частичное обновление пользователя", tags=["Users"]),
    destroy=extend_schema(summary="Удалить пользователя", tags=["Users"]),
)
class UserViewSet(viewsets.ModelViewSet):
    queryset = AppUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if not user.is_staff:
            return AppUser.objects.filter(id=user.id)
        return AppUser.objects.all()

    @extend_schema(
        summary="Профиль текущего пользователя",
        description="Возвращает или обновляет данные пользователя по токену",
        responses={200: UserSerializer},
        methods=["GET", "PATCH"], # Добавь PATCH сюда
        tags=["Users"]
    )
    @action(detail=False, methods=['get', 'patch'])
    def me(self, request):
        user = request.user
        
        # Если это PATCH — обновляем данные
        if request.method == 'PATCH':
            # partial=True позволяет обновлять только присланные поля (например, только username)
            serializer = self.get_serializer(user, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        
        # Если это GET — просто отдаем данные
        serializer = self.get_serializer(user)
        return Response(serializer.data)

    @extend_schema(
        summary="Смена пароля",
        request=ChangePasswordSerializer,
        responses={
            200: ChangePasswordSerializer,
            400: ChangePasswordSerializer,
        },
        tags=["Users"]
    )
    @action(detail=False, methods=['post'], url_path='change-password')
    def change_password(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = request.user
        if not user.check_password(serializer.validated_data["old_password"]):
            return Response({"old_password": "Неверный текущий пароль"}, status=status.HTTP_400_BAD_REQUEST)
        
        user.set_password(serializer.validated_data["new_password"])
        user.save()
        return Response({"detail": "Password changed"}, status=status.HTTP_200_OK)
