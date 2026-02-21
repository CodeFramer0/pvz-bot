import logging

from django.contrib.auth import get_user_model
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from .models import Order, TelegramUser
from .tasks import send_telegram_message

logger = logging.getLogger(__name__)

AppUser = get_user_model()


@receiver(pre_save, sender=Order)
def order_status_pre_save(sender, instance, **kwargs):
    if not instance.pk:
        # новый заказ, старого значения нет
        instance._old_status = None
    else:
        # сохраняем старый статус для post_save
        old = sender.objects.get(pk=instance.pk)
        instance._old_status = old.status


@receiver(post_save, sender=Order)
def order_status_changed(sender, instance, created, **kwargs):
    if created:
        return  # новый заказ — уведомления пока не отправляем

    # проверяем, что статус реально поменялся
    if instance._old_status != instance.status:
        message = (
            f"Статус вашего заказа №{instance.id} изменился на "
            f"'{instance.get_status_display()}'."
        )
        try:
            tg_user = instance.customer.telegram_user
            send_telegram_message.delay(tg_user.user_id, message)
        except TelegramUser.DoesNotExist:
            pass
