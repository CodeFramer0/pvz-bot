from django.db import models
from django.utils.html import mark_safe


class TelegramUser(models.Model):
    name = models.CharField(verbose_name="Имя", max_length=30, default="NoName")
    nick_name = models.CharField(verbose_name="Ник", max_length=32, default="NoName")
    date_join = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата и время создания"
    )
    user_id = models.CharField(max_length=100, verbose_name="User ID", unique=True)
    is_blocked = models.BooleanField(default=False, verbose_name="Заблокирован")
    is_administrator = models.BooleanField(
        default=False,
        verbose_name="Является администратором",
    )

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return f"{self.nick_name} - {self.name} - {self.user_id}"


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
        ("pending", "Ожидает"),
        ("completed", "Завершён"),
        ("barcode_expired", "Штрих код устарел"),
        ("not_arrived", "Ваши товары еще не в Анастасиевке"),
    ]

    customer = models.ForeignKey(
        TelegramUser,
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
        max_length=20, choices=STATUS_CHOICES, default="pending", verbose_name="Статус"
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
