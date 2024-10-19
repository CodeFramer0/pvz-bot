import asyncio
import logging
import os
from celery import shared_task
from django.conf import settings
from django.utils import timezone

from .models import Order
from django.core.management import call_command

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


async def send_telegram_dump():
    date = timezone.now().date()
    output_file = f"robot-{date}.json"

    try:
        with open(output_file, "w") as f:
            call_command("dumpdata", "robot", stdout=f)

        with open(output_file, "rb") as f:
            await settings.BOT.send_document(
                chat_id=settings.DUMP_CHAT_ID, document=f, caption="Дамп robot"
            )

        logger.info(f"Dump sent successfully by task")
        return "Dump sent successfully."

    except Exception as e:
        logger.error(f"Failed to send dump: {e}")
        return f"Failed to send dump: {e}"

    finally:
        if os.path.exists(output_file):
            os.remove(output_file)


@shared_task
def send_telegram_message(user_id, message):
    return asyncio.run(send_message(user_id, message))


@shared_task(bind=True)
def dumpdata_and_send_to_telegram(self):
    return asyncio.run(send_telegram_dump())
