from rest_framework import serializers

from .models import AppUser, Order, PickupPoint, TelegramUser


class TelegramUserSerializer(serializers.ModelSerializer):
    """Serializer для Telegram пользователя"""

    class Meta:
        model = TelegramUser
        fields = "__all__"
        read_only_fields = ["id", "user_id", "date_join"]
        extra_kwargs = {
            "nick_name": {
                "help_text": "Nickname пользователя в Telegram",
            },
            "name": {
                "help_text": "Полное имя пользователя",
            },
            "is_blocked": {
                "help_text": "Заблокирован ли пользователь",
            },
            "is_administrator": {
                "help_text": "Является ли администратором",
            },
        }


class AppUserSerializer(serializers.ModelSerializer):
    """Serializer для пользователя приложения"""

    telegram_user = TelegramUserSerializer(read_only=True)

    class Meta:
        model = AppUser
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "telegram_user",
            "email_verified",
        ]
        read_only_fields = ["id", "email_verified"]
        extra_kwargs = {
            "username": {
                "help_text": "Уникальное имя пользователя для входа",
            },
            "email": {
                "help_text": "Email адрес для входа и уведомлений",
            },
            "first_name": {
                "help_text": "Имя пользователя",
                "required": False,
            },
            "last_name": {
                "help_text": "Фамилия пользователя",
                "required": False,
            },
        }


class PickupPointSerializer(serializers.ModelSerializer):
    """Serializer для пунктов выдачи"""

    class Meta:
        model = PickupPoint
        fields = "__all__"
        extra_kwargs = {
            "address": {
                "help_text": "Полный адрес пункта выдачи",
            },
            "marketplace": {
                "help_text": "Маркетплейс: ozon, wb, yandex, cdek, mail",
            },
            "admin_telegram_user": {
                "help_text": "Telegram аккаунт администратора для уведомлений",
            },
        }


class OrderSerializer(serializers.ModelSerializer):
    """Serializer для заказов пользователя"""

    customer_username = serializers.CharField(
        source="customer.username",
        read_only=True,
        help_text="Имя пользователя (автоматически из customer)",
    )
    pickup_point_address = serializers.CharField(
        source="pickup_point.address",
        read_only=True,
        help_text="Адрес пункта выдачи",
    )
    status_display = serializers.CharField(
        source="get_status_display",
        read_only=True,
        help_text="Читаемое название статуса",
    )

    class Meta:
        model = Order
        fields = [
            "id",
            "customer",
            "customer_username",
            "pickup_point",
            "pickup_point_address",
            "full_name",
            "amount",
            "comment",
            "barcode_image",
            "date_created",
            "status",
            "status_display",
        ]
        read_only_fields = ["id", "date_created", "customer"]
        extra_kwargs = {
            "customer": {
                "help_text": "ID пользователя (автоматически из текущего юзера)",
            },
            "pickup_point": {
                "help_text": "ID пункта выдачи",
            },
            "full_name": {
                "help_text": "ФИО получателя",
            },
            "amount": {
                "help_text": "Сумма заказа от маркетплейса",
            },
            "comment": {
                "help_text": "Комментарий к заказу (опционально)",
                "required": False,
                "allow_blank": True,
            },
            "barcode_image": {
                "help_text": "Изображение штрих-кода заказа (JPEG, PNG)",
            },
            "status": {
                "help_text": "Статус заказа: pending, completed, arrived, и т.д.",
            },
        }

    def validate_amount(self, value):
        """Валидация суммы заказа"""
        if not value or value.strip() == "":
            raise serializers.ValidationError("Сумма заказа не может быть пустой")
        return value

    def validate_full_name(self, value):
        """Валидация ФИО"""
        if len(value.strip()) < 2:
            raise serializers.ValidationError("ФИО должно содержать минимум 2 символа")
        return value
