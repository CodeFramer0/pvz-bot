import asyncio
import base64
import logging
import os
from io import BytesIO

from aiogram.types import InputFile
from celery import shared_task
from django.conf import settings
from django.core.management import call_command
from django.utils import timezone

from .models import Order, TelegramUser

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

async def send_photo(user_id, photo_path, caption: str = None):
    """
    Отправка фото через InputFile
    """
    photo = InputFile(photo_path)
    return await settings.BOT.send_photo(
        chat_id=user_id,
        photo=photo,
        caption=caption
    )


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
    asyncio.run(send_message(user_id, message))


@shared_task(bind=True)
def dumpdata_and_send_to_telegram(self):
    asyncio.run(send_telegram_dump())


@shared_task
def send_mass_telegram(text=None, file_data=None, file_name=None, is_image=False):
    async def send_all():
        for user in TelegramUser.objects.all():
            try:
                if file_data:
                    decoded = base64.b64decode(file_data)
                    file_io = BytesIO(decoded)
                    file_io.name = file_name
                    file_input = InputFile(file_io, filename=file_name)

                    if is_image:
                        await settings.BOT.send_photo(
                            chat_id=user.user_id, photo=file_input, caption=text or None
                        )
                    else:
                        await settings.BOT.send_document(
                            chat_id=user.user_id,
                            document=file_input,
                            caption=text or None,
                        )
                elif text:
                    await settings.BOT.send_message(chat_id=user.user_id, text=text)
            except Exception as e:
                logger.error(f"Ошибка при отправке пользователю {user.user_id}: {e}")

    asyncio.run(send_all())


async def send_arrived_message(order_id):
    try:
        order = Order.objects.get(id=order_id)
        user = order.customer
        pickup = order.pickup_point

        # Красивое сообщение
        message = (
            f"ℹ️ Обновление статуса заказа #{order.id}\n\n"
            f"📦 Ваш заказ готов к выдаче! Вы можете забрать его в выбранном пункте выдачи.\n\n"
            f"🛒 Маркетплейс: {pickup.get_marketplace_display()}\n"
            f"📍 Пункт выдачи: {pickup.address}\n"
            f"🗄  Ячейка №{user.id}"
        )

        # Если есть штрихкод — отправляем картинкой с подписью
        if order.barcode_image:
            await send_photo(user.user_id, order.barcode_image.path, caption=message)
        else:
            await send_message(user.user_id, message)

        logger.info(f"Уведомление отправлено заказу {order.id}")
    except Order.DoesNotExist:
        logger.warning(f"Заказ {order_id} не найден")

@shared_task
def send_order_arrived_notification(order_id):
    return asyncio.run(send_arrived_message(order_id))