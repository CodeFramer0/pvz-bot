from django.contrib import admin

from .forms import PickPointForm
from .models import *


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
    search_fields = ("nick_name", "name", "user_id")
    list_filter = ("is_administrator", "date_join")
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
    list_filter = ("status", "pickup_point", "date_created")
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
