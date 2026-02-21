from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from .callback_data import (cb_order_action, cb_order_marketplace_action,
                            cb_order_pickup_point_action)


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


def marketplaces(available_marketplaces: list):
    """
    available_marketplaces — список словарей вида:
    [{"id": 1, "code": "ozon", "name": "Ozon 🔵"}, ...]
    """
    keyboard = InlineKeyboardMarkup(row_width=1)

    for mp in available_marketplaces:
        keyboard.insert(
            InlineKeyboardButton(
                text=mp["name"],
                callback_data=cb_order_marketplace_action.new(
                    action="choose_marketplace",
                    marketplace=mp["code"],
                    marketplace_id=mp["id"],
                ),
            )
        )

    keyboard.insert(
        InlineKeyboardButton(
            text="Отменить ❌",
            callback_data=cb_order_action.new(action="cancel")
        )
    )
    return keyboard


def pickup_points(points):
    keyboard = InlineKeyboardMarkup(row_width=1)

    if isinstance(points, list):
        for point in points:
            # берём первый маркетплейс или None
            marketplace = (
                point["marketplaces"][0]["code"] if point["marketplaces"] else ""
            )
            keyboard.insert(
                InlineKeyboardButton(
                    text=point["address"],
                    callback_data=cb_order_pickup_point_action.new(
                        action="choose_pickup_point",
                        marketplace=marketplace,
                        pickup_point_id=point["id"],
                    ),
                )
            )
    else:
        marketplace = (
            points["marketplaces"][0]["code"] if points["marketplaces"] else ""
        )
        keyboard.insert(
            InlineKeyboardButton(
                text=points["address"],
                callback_data=cb_order_pickup_point_action.new(
                    action="choose_pickup_point",
                    marketplace=marketplace,
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
