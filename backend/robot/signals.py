import logging

from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Order
from .tasks import send_telegram_message

logger = logging.getLogger(__name__)


@receiver(post_save, sender=Order)
def order_status_changed(sender, instance, created, **kwargs):
    if not created:
        message = f"Статус вашего заказа №{instance.id} изменился на '{instance.get_status_display()}'."
        send_telegram_message.delay(instance.customer.user_id, message)
