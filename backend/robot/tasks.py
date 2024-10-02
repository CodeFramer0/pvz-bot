import asyncio
import logging

from celery import shared_task
from django.conf import settings
from django.utils import timezone

from .models import Order

logger = logging.getLogger(__name__)


@shared_task
def expire_old_orders():
    now = timezone.now()

    old_orders = Order.objects.filter(
        status="pending", date_created__lt=now - timezone.timedelta(hours=24)
    )

    old_orders.update(status="barcode_expired")


async def send_message(user_id, message):
    return await settings.BOT.send_message(chat_id=user_id, text=message)


@shared_task
def send_telegram_message(user_id, message):
    return asyncio.run(send_message(user_id, message))
