from io import BytesIO

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.utils.exceptions import (MessageCantBeDeleted,
                                      MessageToForwardNotFound)
from api.base import APIError
from keyboards.inline import order_keyboards
from keyboards.inline.callback_data import (cb_order_action,
                                            cb_order_marketplace_action,
                                            cb_order_pickup_point_action)
from loader import (bot, dp, marketplace_api, order_api, pickup_point_api,
                    telegram_user_api)
from states.order import OrderStates
from utils.utils import delete_message

from .start import back_to_main_menu


@dp.message_handler(content_types=["photo"], state="*")
async def handle_photo(message: types.Message, state: FSMContext, user):
    photo = message.photo[-1]
    file_id = photo.file_id

    await state.update_data(file_id=file_id)
    await message.delete()
    message = await message.answer(
        "Отлично!\n<strong>Теперь введите ФИО.</strong>",
        reply_markup=order_keyboards.cancel(),
    )
    await OrderStates.waiting_for_full_name.set()
    await state.update_data(message_id=message.message_id)


@dp.message_handler(state=OrderStates.waiting_for_full_name)
async def handle_full_name(message: types.Message, user, state: FSMContext):
    await message.delete()
    if message.text == "/start":
        return await back_to_main_menu(message, user, state)
    full_name = message.text
    await state.update_data(full_name=full_name)
    user_data = await state.get_data()
    message_id = user_data.get("message_id")
    await delete_message(chat_id=message.chat.id, message_id=message_id)
    available_marketplaces = await marketplace_api.get()
    message = await message.answer(
        "<strong>Теперь выберите маркетплейс.</strong>",
        reply_markup=order_keyboards.marketplaces(available_marketplaces),
    )
    await OrderStates.waiting_for_marketplace.set()
    await state.update_data(message_id=message.message_id)


@dp.callback_query_handler(
    cb_order_marketplace_action.filter(action="choose_marketplace"),
    state="*",
)
async def choose_marketplace(
    query: types.CallbackQuery, callback_data: dict, state: FSMContext
):
    await query.answer("")
    marketplace = callback_data["marketplace"]
    marketplace_id = callback_data["marketplace_id"]
    pickup_points = await pickup_point_api.get(params={"marketplace": marketplace})
    await delete_message(
        chat_id=query.message.chat.id, message_id=query.message.message_id
    )
    message = await query.message.answer(
        "Супер!\n<strong>Теперь выберите один из доступных пунктов выдачи заказов.</strong>",
        reply_markup=order_keyboards.pickup_points(pickup_points),
    )

    await OrderStates.waiting_for_pickup_point.set()
    await state.update_data(
        message_id=message.message_id,
        marketplace=marketplace,
        marketplace_id=marketplace_id,
    )


@dp.callback_query_handler(
    cb_order_pickup_point_action.filter(action="choose_pickup_point"),
    state="*",
)
async def handle_pickup_point(
    query: types.CallbackQuery, callback_data: dict, state: FSMContext
):
    await query.answer("")
    await state.update_data(pickup_point_id=callback_data["pickup_point_id"])
    await delete_message(
        chat_id=query.message.chat.id, message_id=query.message.message_id
    )
    message = await query.message.answer(
        "Осталось совсем немного :) \n" "Введите пожалуйста сумму Вашего заказа.",
        reply_markup=order_keyboards.cancel(),
    )
    await OrderStates.waiting_for_amount.set()
    await state.update_data(message_id=message.message_id)


@dp.message_handler(state=OrderStates.waiting_for_amount)
async def handle_amount(message: types.Message, state: FSMContext, user):
    await message.delete()
    if message.text == "/start":
        return await back_to_main_menu(message, user, state)
    amount = message.text
    await state.update_data(amount=amount)
    user_data = await state.get_data()
    message_id = user_data.get("message_id")
    await delete_message(chat_id=message.chat.id, message_id=message_id)
    message = await message.answer(
        "И последний шаг:\n"
        "<strong>Вы можете добавить комментарий к Вашему заказу.\n\nЕсли комментарий Вам не нужен нажмите на кнопку 'пропустить'.</strong>",
        reply_markup=order_keyboards.skip(),
    )
    await OrderStates.waiting_for_comment.set()
    await state.update_data(message_id=message.message_id)


@dp.callback_query_handler(
    cb_order_action.filter(action="cancel"),
    state="*",
)
async def cancel(query: types.CallbackQuery, state: FSMContext, user):
    await query.answer("")
    await back_to_main_menu(query.message, state, user)


async def create_order(chat_id: int, user: dict, user_data: dict, comment: str = ""):
    full_name = user_data.get("full_name")
    amount = user_data.get("amount")
    file_id = user_data.get("file_id")
    pickup_point_id = user_data.get("pickup_point_id")
    marketplace_id = user_data.get("marketplace_id")
    marketplace_name = user_data.get("marketplace")

    try:
        customer_id = int(user["app_user"])
    except (TypeError, ValueError):
        await bot.send_message(chat_id, "Ошибка: неверный ID пользователя.")
        return None

    # Получаем объекты PickupPoint и Marketplace
    pickup_point = await pickup_point_api.get(id=pickup_point_id)
    marketplace = await marketplace_api.get(id=marketplace_id)

    # Загружаем файл штрих-кода
    image_data = await bot.download_file_by_id(file_id)
    image_bytes = BytesIO(image_data.getvalue())
    image_bytes.name = "image.jpg"

    # Создаем заказ через API
    try:
        order = await order_api.post_multipart(
            json={
                "full_name": full_name,
                "pickup_point_id": pickup_point_id,
                "marketplace_id": marketplace_id,
                "customer_id": customer_id,
                "amount": amount,
                "comment": comment,
            },
            files={"barcode_image": image_bytes},
        )
    except APIError as e:
        detail = e.detail
        if isinstance(detail, dict):
            messages = []
            for k, v in detail.items():
                if isinstance(v, list):
                    messages.append(f"{k}: {', '.join(v)}")
                else:
                    messages.append(f"{k}: {v}")
            await bot.send_message(
                chat_id, "Ошибка при создании заказа:\n" + "\n".join(messages)
            )
        else:
            await bot.send_message(chat_id, f"Ошибка при создании заказа: {detail}")
        return None

    # Отправляем подтверждение пользователю
    await bot.send_photo(
        chat_id,
        photo=image_data,
        caption=(
            f"<strong>Ваш заказ №{order['id']} успешно создан! 🎉</strong>\n"
            f"<strong>ФИО:</strong> {order['full_name']}\n"
            f"<strong>Маркетплейс:</strong> {marketplace_name}\n"
            f"<strong>Адрес:</strong> {pickup_point['address']}\n"
            f"<strong>Сумма заказа:</strong> {order['amount']}\n"
            f"<strong>Комментарий к заказу:</strong> {order['comment']}\n\n"
            f"<strong>Ячейка:</strong> №{user['id']} (необходим при получении)\n\n"
            "Как только статус Вашего заказа изменится, <strong>я пришлю Вам уведомление!</strong>"
        ),
    )

    return order


@dp.message_handler(state=OrderStates.waiting_for_comment)
async def handle_comment(message: types.Message, state: FSMContext, user):
    await message.delete()
    if message.text == "/start":
        return await back_to_main_menu(message, user, state)
    user_data = await state.get_data()
    await create_order(message.chat.id, user, user_data, comment=message.text)
    await delete_message(chat_id=message.chat.id, message_id=user_data["message_id"])
    await state.finish()


@dp.callback_query_handler(cb_order_action.filter(action="skip"), state="*")
async def skip(query: types.CallbackQuery, state: FSMContext, user):
    await query.answer("")
    user_data = await state.get_data()
    await create_order(query.message.chat.id, user, user_data, comment="")
    await delete_message(
        chat_id=query.message.chat.id, message_id=user_data["message_id"]
    )
    await state.finish()
