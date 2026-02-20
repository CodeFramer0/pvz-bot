from django.contrib import admin, messages
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from .forms import PickPointForm
from .models import *
from .tasks import *


@admin.register(AppUser)
class AppUserAdmin(UserAdmin):
    model = AppUser
    list_display = ("username", "email", "phone_number", "is_staff", "is_active")
    list_filter = ("is_staff", "is_active")
    fieldsets = (
        (None, {"fields": ("username", "email", "password", "phone_number")}),
        (
            "Permissions",
            {
                "fields": (
                    "is_staff",
                    "is_active",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "username",
                    "email",
                    "phone_number",
                    "password1",
                    "password2",
                    "is_staff",
                    "is_active",
                ),
            },
        ),
    )
    search_fields = ("email", "username", "phone_number")
    ordering = ("email",)


@admin.register(TelegramUser)
class TelegramUserAdmin(admin.ModelAdmin):
    list_display = (
        "nick_name",
        "name",
        "id",
        "user_id",
        "date_join",
        "is_administrator",
    )
    search_fields = ("id","nick_name", "name", "user_id")
    list_filter = ("is_administrator","date_join")
    ordering = ("-date_join",)

    def has_add_permission(self, request, obj=None):
        return False


@admin.register(PickupPoint)
class PickupPointAdmin(admin.ModelAdmin):
    form = PickPointForm
    list_display = (
        "address",
        "marketplace",
    )
    list_filter = ("marketplace",)
    search_fields = ("address",)
    ordering = ("marketplace", "address")


class StatusFilter(admin.SimpleListFilter):
    title = _("Статус")
    parameter_name = "status"

    def lookups(self, request, model_admin):
        return (
            ("not_ready", _("Не готовы к выдаче")),  # кастомная группа
            ("pending", _("Ожидают")),  # конкретный статус
            ("completed", _("Собраны и погружены на ближайшую доставку")),
            ("barcode_expired", _("Штрих код устарел")),
            ("not_arrived_goods", _("Товары еще не в Анастасиевке")),
            ("insufficient_funds", _("Недостаточно средств")),
            ("card_not_linked", _("Банковская карта не привязана")),
            ("contact_manager", _("Свяжитесь с менеджером")),
            ("processed", _("Обработаны.")),
            ("arrived", _("Готовы к выдаче")),
        )

    def queryset(self, request, queryset):
        if self.value() == "not_ready":
            return queryset.exclude(status="arrived")  # все, кроме готовых
        if self.value() == "pending":
            return queryset.filter(status="pending")  # только pending
        if self.value():
            return queryset.filter(status=self.value())
        return queryset


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "customer",
        "cell_id",
        "id",
        "pickup_point",
        "full_name",
        "date_created",
        "status",
        "image_tag",
    )
    list_filter = (
        StatusFilter,
        "pickup_point",
        "date_created",
    )
    search_fields = (
        "full_name",
        "pickup_point__address",
        "customer__id",
        "customer__nick_name",
        "customer__name",
    )
    ordering = ("-date_created",)
    readonly_fields = (
        "customer",
        "image_tag",
        "date_created",
        "cell_id",
    )
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "customer",
                    "pickup_point",
                    "full_name",
                    "amount",
                    "comment",
                    "barcode_image",
                    "status",
                    "date_created",
                    "cell_id",
                    "image_tag",
                )
            },
        ),
    )

    actions = ["mark_as_arrived"]

    @admin.action(
        description="Отметить выбранные заказы как 'Прибывший' и уведомить клиента"
    )
    def mark_as_arrived(self, request, queryset):
        # Проверяем, что поле status корректное
        pending_orders = queryset.exclude(status="arrived")

        # Получаем список id, чтобы отправлять уведомления
        order_ids = pending_orders.values_list("id", flat=True)
        for order_id in order_ids:
            logging.info(f"Отправка уведомления заказу {order_id}")
            send_order_arrived_notification.delay(order_id)

        updated_count = pending_orders.update(status="arrived")
        self.message_user(
            request,
            f"{updated_count} заказ(ов) отмечены как 'Прибывший' и уведомления отправлены.",
            messages.SUCCESS,
        )
