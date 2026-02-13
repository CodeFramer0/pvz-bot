import base64
import mimetypes
import random

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.http import HttpResponseForbidden
from django.shortcuts import render
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import (OpenApiExample, OpenApiParameter,
                                   OpenApiResponse, extend_schema)
from rest_framework import status, viewsets
from rest_framework.authentication import SessionAuthentication
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .filters import OrderFilter, PickupPointFilter, TelegramUserFilter
from .forms import NewsletterForm
from .models import AppUser, Order, PickupPoint, TelegramUser
from .serializers import (AppUserSerializer, OrderSerializer,
                          PickupPointSerializer, TelegramUserSerializer)
from .tasks import send_mass_telegram


@extend_schema(tags=["Authentication"])
class AuthViewSet(viewsets.ViewSet):
    """Аутентификация"""

    permission_classes = [AllowAny]

    def get_tokens_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        return {
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "user": AppUserSerializer(user).data,
        }

    @extend_schema(
        operation_id="auth_register",
        summary="Регистрация по Email",
        description="Регистрация нового пользователя с отправкой кода на email",
        request={
            "application/json": {
                "type": "object",
                "required": ["username", "email", "password"],
                "properties": {
                    "username": {
                        "type": "string",
                        "description": "Уникальное имя пользователя",
                        "example": "john_doe",
                    },
                    "email": {
                        "type": "string",
                        "format": "email",
                        "description": "Email адрес",
                        "example": "john@example.com",
                    },
                    "password": {
                        "type": "string",
                        "description": "Пароль (мин. 6 символов)",
                        "example": "password123",
                    },
                    "telegram_user_id": {
                        "type": "string",
                        "nullable": True,
                        "description": "ID Telegram пользователя (опционально)",
                        "example": "123456789",
                    },
                },
            }
        },
    )
    @action(detail=False, methods=["post"], permission_classes=[AllowAny])
    def register(self, request):
        username = request.data.get("username")
        email = request.data.get("email")
        password = request.data.get("password")
        telegram_user_id = request.data.get("telegram_user_id")

        if not username or not email or not password:
            return Response(
                {"error": "Требуется username, email и password"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if AppUser.objects.filter(username=username).exists():
            return Response(
                {"error": "Username уже занят"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if AppUser.objects.filter(email=email).exists():
            return Response(
                {"error": "Email уже зарегистрирован"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        verification_code = "".join([str(random.randint(0, 9)) for _ in range(6)])
        user = AppUser.objects.create_user(
            username=username,
            email=email,
            password=password,
            verification_code=verification_code,
            is_active=False,
        )

        if telegram_user_id:
            try:
                telegram_user = TelegramUser.objects.get(user_id=telegram_user_id)
                telegram_user.app_user = user
                telegram_user.save()
            except TelegramUser.DoesNotExist:
                pass

        return Response(
            {
                "status": "verification_needed",
                "message": "Код подтверждения отправлен на почту",
                "user_id": user.id,
                "email": user.email,
            },
            status=status.HTTP_201_CREATED,
        )

    @extend_schema(
        operation_id="auth_verify_email",
        summary="✅ Подтверждение Email",
        request={
            "application/json": {
                "type": "object",
                "required": ["user_id", "code"],
                "properties": {
                    "user_id": {
                        "type": "integer",
                        "description": "ID пользователя из register",
                        "example": 1,
                    },
                    "code": {
                        "type": "string",
                        "description": "6-значный код из email",
                        "example": "123456",
                    },
                },
            }
        },
    )
    @action(detail=False, methods=["post"], permission_classes=[AllowAny])
    def verify_email(self, request):
        user_id = request.data.get("user_id")
        verification_code = request.data.get("code")

        try:
            user = AppUser.objects.get(id=user_id)
        except AppUser.DoesNotExist:
            return Response(
                {"error": "Пользователь не найден"},
                status=status.HTTP_404_NOT_FOUND,
            )

        if user.verification_code != verification_code:
            return Response(
                {"error": "Неверный код"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user.email_verified = True
        user.is_active = True
        user.verification_code = None
        user.save()

        return Response(
            {
                "status": "success",
                "message": "Email подтвержден",
                **self.get_tokens_for_user(user),
            }
        )

    @extend_schema(
        operation_id="auth_login",
        summary="Вход по Email+Пароль",
        request={
            "application/json": {
                "type": "object",
                "required": ["email", "password"],
                "properties": {
                    "email": {
                        "type": "string",
                        "format": "email",
                        "description": "Email адрес",
                        "example": "john@example.com",
                    },
                    "password": {
                        "type": "string",
                        "description": "Пароль",
                        "example": "password123",
                    },
                },
            }
        },
    )
    @action(detail=False, methods=["post"], permission_classes=[AllowAny])
    def login(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        if not email or not password:
            return Response(
                {"error": "Требуется email и password"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            user = AppUser.objects.get(email=email)
        except AppUser.DoesNotExist:
            return Response(
                {"error": "Пользователь не найден"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        if not user.check_password(password):
            return Response(
                {"error": "Неверный пароль"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        if not user.is_active:
            return Response(
                {"error": "Аккаунт неактивен. Подтвердите email"},
                status=status.HTTP_403_FORBIDDEN,
            )

        return Response(
            {
                "status": "success",
                **self.get_tokens_for_user(user),
            }
        )

    @extend_schema(
        operation_id="auth_telegram_login",
        summary="Вход через Telegram",
        request={
            "application/json": {
                "type": "object",
                "required": ["telegram_user_id"],
                "properties": {
                    "telegram_user_id": {
                        "type": "string",
                        "description": "Telegram User ID",
                        "example": "123456789",
                    },
                },
            }
        },
    )
    @action(detail=False, methods=["post"], permission_classes=[AllowAny])
    def telegram_login(self, request):
        telegram_user_id = request.data.get("telegram_user_id")

        if not telegram_user_id:
            return Response(
                {"error": "Требуется telegram_user_id"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            telegram_user = TelegramUser.objects.get(user_id=telegram_user_id)
        except TelegramUser.DoesNotExist:
            return Response(
                {"error": "Telegram пользователь не найден"},
                status=status.HTTP_404_NOT_FOUND,
            )

        if not telegram_user.app_user:
            app_user = AppUser.objects.create_user(
                username=f"tg_{telegram_user_id}",
                email=f"tg_{telegram_user_id}@pvz.local",
                email_verified=True,
                is_active=True,
            )
            telegram_user.app_user = app_user
            telegram_user.save()
        else:
            app_user = telegram_user.app_user

        return Response(
            {
                "status": "success",
                **self.get_tokens_for_user(app_user),
            }
        )

    @extend_schema(
        operation_id="auth_link_telegram",
        summary="Привязать Telegram",
        request={
            "application/json": {
                "type": "object",
                "required": ["telegram_user_id"],
                "properties": {
                    "telegram_user_id": {
                        "type": "string",
                        "description": "Telegram User ID",
                        "example": "123456789",
                    },
                },
            }
        },
    )
    @action(detail=False, methods=["post"], permission_classes=[IsAuthenticated])
    def link_telegram(self, request):
        telegram_user_id = request.data.get("telegram_user_id")

        if not telegram_user_id:
            return Response(
                {"error": "Требуется telegram_user_id"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            telegram_user = TelegramUser.objects.get(user_id=telegram_user_id)
        except TelegramUser.DoesNotExist:
            return Response(
                {"error": "Telegram пользователь не найден"},
                status=status.HTTP_404_NOT_FOUND,
            )

        if telegram_user.app_user and telegram_user.app_user != request.user:
            return Response(
                {"error": "Этот Telegram уже привязан к другому аккаунту"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        telegram_user.app_user = request.user
        telegram_user.save()

        return Response(
            {
                "status": "success",
                "message": "Telegram привязан",
                "telegram_user": TelegramUserSerializer(telegram_user).data,
            }
        )

    @extend_schema(
        operation_id="auth_refresh_token",
        summary="🔄 Обновить Access Token",
        request={
            "application/json": {
                "type": "object",
                "required": ["refresh"],
                "properties": {
                    "refresh": {
                        "type": "string",
                        "description": "Refresh token",
                        "example": "eyJ0eXAiOiJKV1QiLCJhbGc...",
                    },
                },
            }
        },
    )
    @action(detail=False, methods=["post"], permission_classes=[AllowAny])
    def refresh_token(self, request):
        refresh = request.data.get("refresh")

        if not refresh:
            return Response(
                {"error": "Требуется refresh token"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            refresh_token = RefreshToken(refresh)
            return Response(
                {
                    "status": "success",
                    "access": str(refresh_token.access_token),
                    "refresh": str(refresh_token),
                }
            )
        except Exception:
            return Response(
                {"error": "Неверный refresh token"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

    @extend_schema(
        operation_id="auth_me",
        summary="👤 Получить Текущего Пользователя",
    )
    @action(detail=False, methods=["get"], permission_classes=[IsAuthenticated])
    def me(self, request):
        return Response(AppUserSerializer(request.user).data)

    @extend_schema(
        operation_id="auth_resend_code",
        summary="📧 Отправить Код Подтверждения",
        request={
            "application/json": {
                "type": "object",
                "required": ["email"],
                "properties": {
                    "email": {
                        "type": "string",
                        "format": "email",
                        "description": "Email адрес",
                    },
                },
            }
        },
    )
    @action(detail=False, methods=["post"], permission_classes=[AllowAny])
    def resend_code(self, request):
        email = request.data.get("email")

        if not email:
            return Response(
                {"error": "Требуется email"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            user = AppUser.objects.get(email=email)
        except AppUser.DoesNotExist:
            return Response(
                {"error": "Пользователь с таким email не найден"},
                status=status.HTTP_404_NOT_FOUND,
            )

        verification_code = "".join([str(random.randint(0, 9)) for _ in range(6)])
        user.verification_code = verification_code
        user.save()

        try:
            send_mail(
                "Код подтверждения PVZ Bot",
                f"Ваш код подтверждения: {verification_code}",
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
            )
        except Exception as e:
            return Response(
                {"error": f"Ошибка отправки email: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        return Response(
            {
                "status": "success",
                "message": "Код подтверждения отправлен на почту",
                "email": email,
            }
        )


@extend_schema(tags=["User Profile"])
class AppUserViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = AppUserSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication]

    def get_queryset(self):
        return AppUser.objects.filter(id=self.request.user.id)

    @extend_schema(
        operation_id="user_update_profile",
        summary="✏️ Обновить Профиль",
        request={
            "application/json": {
                "type": "object",
                "properties": {
                    "email": {
                        "type": "string",
                        "format": "email",
                        "description": "Новый email",
                        "example": "newemail@example.com",
                    },
                    "first_name": {
                        "type": "string",
                        "description": "Имя",
                        "example": "John",
                    },
                    "last_name": {
                        "type": "string",
                        "description": "Фамилия",
                        "example": "Doe",
                    },
                },
            }
        },
    )
    @action(
        detail=False, methods=["put", "patch"], permission_classes=[IsAuthenticated]
    )
    def update_profile(self, request):
        user = request.user
        email = request.data.get("email")
        first_name = request.data.get("first_name")
        last_name = request.data.get("last_name")

        if email and email != user.email:
            if AppUser.objects.filter(email=email).exclude(id=user.id).exists():
                return Response(
                    {"error": "Email уже используется"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            user.email = email

        if first_name:
            user.first_name = first_name
        if last_name:
            user.last_name = last_name

        user.save()
        return Response(AppUserSerializer(user).data)


@extend_schema(
    tags=["Telegram Users"],
    parameters=[
        OpenApiParameter(
            name="page",
            description="Номер страницы",
            required=False,
            type=OpenApiTypes.INT,
        ),
        OpenApiParameter(
            name="page_size",
            description="Количество элементов на странице",
            required=False,
            type=OpenApiTypes.INT,
        ),
        OpenApiParameter(
            name="nick_name",
            description="Фильтр по нику",
            required=False,
            type=OpenApiTypes.STR,
        ),
        OpenApiParameter(
            name="is_administrator",
            description="Только администраторы",
            required=False,
            type=OpenApiTypes.BOOL,
        ),
        OpenApiParameter(
            name="is_blocked",
            description="Только заблокированные",
            required=False,
            type=OpenApiTypes.BOOL,
        ),
    ],
)
class TelegramUserViewSet(viewsets.ModelViewSet):
    serializer_class = TelegramUserSerializer
    queryset = TelegramUser.objects.all().order_by("id")
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication]
    filterset_class = TelegramUserFilter


@extend_schema(
    tags=["Pickup Points"],
    parameters=[
        OpenApiParameter(
            name="page",
            description="Номер страницы",
            required=False,
            type=OpenApiTypes.INT,
        ),
        OpenApiParameter(
            name="page_size",
            description="Количество элементов на странице",
            required=False,
            type=OpenApiTypes.INT,
        ),
        OpenApiParameter(
            name="marketplace",
            description="Фильтр по маркетплейсу (ozon, wb, yandex, cdek, mail)",
            required=False,
            type=OpenApiTypes.STR,
        ),
        OpenApiParameter(
            name="address",
            description="Поиск по адресу",
            required=False,
            type=OpenApiTypes.STR,
        ),
    ],
)
class PickupPointViewSet(viewsets.ModelViewSet):
    serializer_class = PickupPointSerializer
    queryset = PickupPoint.objects.all().order_by("id")
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication]
    filterset_class = PickupPointFilter


@extend_schema(
    tags=["Orders"],
    parameters=[
        OpenApiParameter(
            name="page",
            description="Номер страницы",
            required=False,
            type=OpenApiTypes.INT,
        ),
        OpenApiParameter(
            name="page_size",
            description="Количество элементов на странице",
            required=False,
            type=OpenApiTypes.INT,
        ),
        OpenApiParameter(
            name="status",
            description="Фильтр по статусу (pending, completed, arrived и т.д.)",
            required=False,
            type=OpenApiTypes.STR,
        ),
        OpenApiParameter(
            name="full_name",
            description="Поиск по ФИО",
            required=False,
            type=OpenApiTypes.STR,
        ),
        OpenApiParameter(
            name="ordering",
            description="Сортировка (-date_created, amount и т.д.)",
            required=False,
            type=OpenApiTypes.STR,
        ),
    ],
)
class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication]
    filterset_class = OrderFilter

    def get_queryset(self):
        return Order.objects.filter(customer=self.request.user).order_by(
            "-date_created"
        )

    def perform_create(self, serializer):
        serializer.save(customer=self.request.user)

    @extend_schema(
        operation_id="order_my_orders",
        summary="📦 Мои Заказы",
        parameters=[
            OpenApiParameter(
                name="page",
                description="Номер страницы",
                required=False,
                type=OpenApiTypes.INT,
            ),
            OpenApiParameter(
                name="page_size",
                description="Количество элементов на странице",
                required=False,
                type=OpenApiTypes.INT,
            ),
        ],
    )
    @action(detail=False, methods=["get"])
    def my_orders(self, request):
        orders = self.get_queryset()
        serializer = self.get_serializer(orders, many=True)
        return Response(serializer.data)


@login_required(login_url="/admin/login/")
def newsletter_view(request):
    if not request.user.is_staff:
        return HttpResponseForbidden("Нет доступа.")

    if request.method == "POST":
        form = NewsletterForm(request.POST, request.FILES)
        if form.is_valid():
            text = form.cleaned_data["text"]
            file = request.FILES.get("file")

            file_data = None
            file_name = None
            is_image = False

            if file:
                content = file.read()
                file_data = base64.b64encode(content).decode("utf-8")
                file_name = file.name
                mime_type, _ = mimetypes.guess_type(file.name)
                is_image = mime_type and mime_type.startswith("image")

            send_mass_telegram.delay(
                text=text, file_data=file_data, file_name=file_name, is_image=is_image
            )

            return render(
                request,
                "newsletter_form.html",
                {"form": NewsletterForm(), "message": "Рассылка запущена!"},
            )
    else:
        form = NewsletterForm()

    return render(request, "newsletter_form.html", {"form": form})
