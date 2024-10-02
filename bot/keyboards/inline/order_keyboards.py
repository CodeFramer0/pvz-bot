from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from .callback_data import (
    cb_order_action,
    cb_order_marketplace_action,
    cb_order_pickup_point_action,
)


def cancel():
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.insert(
        InlineKeyboardButton(
            text="Отменить ❌", callback_data=cb_order_action.new(action="cancel")
        )
    )
    return keyboard


def skip():
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.insert(
        InlineKeyboardButton(
            text="Пропустить ➡️", callback_data=cb_order_action.new(action="skip")
        )
    )
    keyboard.insert(
        InlineKeyboardButton(
            text="Отменить ❌", callback_data=cb_order_action.new(action="cancel")
        )
    )
    return keyboard


def marketplaces():
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.insert(
        InlineKeyboardButton(
            text="Ozon 🔵 ",
            callback_data=cb_order_marketplace_action.new(
                action="choose_marketplace", marketplace="ozon"
            ),
        )
    )
    keyboard.insert(
        InlineKeyboardButton(
            text="Wildberries 🟣",
            callback_data=cb_order_marketplace_action.new(
                action="choose_marketplace", marketplace="wb"
            ),
        )
    )
    keyboard.insert(
        InlineKeyboardButton(
            text="Yandex Market 🟡",
            callback_data=cb_order_marketplace_action.new(
                action="choose_marketplace", marketplace="yandex"
            ),
        )
    )
    keyboard.insert(
        InlineKeyboardButton(
            text="Cdek 🟢",
            callback_data=cb_order_marketplace_action.new(
                action="choose_marketplace", marketplace="cdek"
            ),
        )
    )
    keyboard.insert(
        InlineKeyboardButton(
            text="Отменить ❌", callback_data=cb_order_action.new(action="cancel")
        )
    )
    return keyboard


def pickup_points(points):
    keyboard = InlineKeyboardMarkup(row_width=1)
    if isinstance(points, list):
        for point in points:
            keyboard.insert(
                InlineKeyboardButton(
                    text=point["address"],
                    callback_data=cb_order_pickup_point_action.new(
                        action="choose_pickup_point",
                        marketplace=point["marketplace"],
                        pickup_point_id=point["id"],
                    ),
                )
            )
    else:
        keyboard.insert(
            InlineKeyboardButton(
                text=points["address"],
                callback_data=cb_order_pickup_point_action.new(
                    action="choose_pickup_point",
                    marketplace=points["marketplace"],
                    pickup_point_id=points["id"],
                ),
            )
        )
    keyboard.insert(
        InlineKeyboardButton(
            text="Отменить ❌", callback_data=cb_order_action.new(action="cancel")
        )
    )
    return keyboard
