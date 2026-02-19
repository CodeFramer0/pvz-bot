import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.html import mark_safe
from django.utils.translation import gettext_lazy as _


class AppUser(AbstractUser):
    verification_code = models.CharField(max_length=6, blank=True, null=True)
    password_reset_code = models.CharField(max_length=32, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    email = models.EmailField(unique=True, null=True, blank=True)
    phone_number = models.CharField(max_length=20, unique=True, null=True, blank=True)
    email_verified = models.BooleanField(default=False)

    USERNAME_FIELD = "email"  # ← ИЗМЕНИ НА EMAIL
    REQUIRED_FIELDS = ["username"]  # ← username теперь в required

    def __str__(self):
        return f"{self.username} ({self.email})"

    class Meta:
        verbose_name = "App пользователь"
        verbose_name_plural = "App пользователи"


class TelegramUser(models.Model):
    """Telegram пользователь - привязан к AppUser"""

    app_user = models.OneToOneField(
        AppUser,
        on_delete=models.CASCADE,
        related_name="telegram_user",
        null=True,
        blank=True,
        verbose_name="Привязанный app пользователь",
    )
    name = models.CharField(verbose_name="Имя", max_length=512, default="NoName")
    nick_name = models.CharField(verbose_name="Ник", max_length=32, default="NoName")
    date_join = models.DateTimeField(auto_now_add=True)
    user_id = models.CharField(
        max_length=100, verbose_name="Telegram User ID", unique=True
    )
    is_blocked = models.BooleanField(default=False)
    is_administrator = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Telegram пользователь"
        verbose_name_plural = "Telegram пользователи"

    def __str__(self):
        return f"{self.nick_name} - {self.name}"


class PickupPoint(models.Model):
    MARKETPLACE_CHOICES = [
        ("ozon", "Озон"),
        ("wb", "ВБ"),
        ("yandex", "Яндекс Маркет"),
        ("cdek", "СДЭК"),
        ("mail", "Почта России +150₽"),
    ]

    address = models.CharField(verbose_name="Адрес пункта выдачи", max_length=255)
    marketplace = models.CharField(
        verbose_name="Название маркетплейса", max_length=50, choices=MARKETPLACE_CHOICES
    )
    admin_telegram_user = models.ForeignKey(
        TelegramUser,
        on_delete=models.CASCADE,
        related_name="notification_accounts",
        verbose_name="Аккаунт для уведомлений",
    )

    class Meta:
        verbose_name = "Пункт выдачи"
        verbose_name_plural = "Пункты выдачи"

    def __str__(self):
        return f"{self.marketplace} - {self.address}"


class Order(models.Model):
    STATUS_CHOICES = [
        ("Created", _("В сборке")),
        ("Processed", _("Обработан")),
        ("TransferringToDelivery", _("Передается в доставку")),
        ("BarcodeExpired", _("Штрих код устарел")),
        ("NotArrivedGoods", _("Ваши товары еще не в Анастасиевке")),
        ("InsufficientFunds", _("Недостаточно средств")),
        ("CardNotLinked", _("Банковская карта не привязана")),
        ("ContactManager", _("Свяжитесь с менеджером.")),
        ("AvailableForPickup", _("Готов к выдаче")),
        ("Received",_("Заказ получен в пункте выдачи"))
    ]

    customer = models.ForeignKey(
        AppUser,  # Меняем на AppUser вместо TelegramUser
        on_delete=models.CASCADE,
        related_name="orders",
        verbose_name="Пользователь",
    )
    pickup_point = models.ForeignKey(
        PickupPoint,
        on_delete=models.CASCADE,
        related_name="orders",
        verbose_name="Пункт выдачи",
    )
    full_name = models.CharField(verbose_name="ФИО", max_length=100)
    amount = models.CharField(verbose_name="Сумма заказа", max_length=128, default="0")
    comment = models.TextField(
        verbose_name="Комментарий к заказу", blank=True, null=True
    )
    barcode_image = models.ImageField(
        upload_to="barcodes/",
        verbose_name="Изображение штрих-кода",
    )
    date_created = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    status = models.CharField(
        max_length=128, choices=STATUS_CHOICES, default="pending", verbose_name="Статус"
    )

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

    def image_tag(self):
        if self.barcode_image:
            return mark_safe(
                f'<a target="_blank" href="{self.barcode_image.url}"><img src="{self.barcode_image.url}" style="width: 300px; height: auto;" /></a>'
            )
        return "Нет изображения"

    def cell_id(self):
        return self.customer.id

    image_tag.short_description = "Предварительный просмотр"
    cell_id.short_description = "Номер ячейки"

    def __str__(self):
        return f"Заказ {self.id} (номер ячейки {self.customer.id}) от {self.customer}"
