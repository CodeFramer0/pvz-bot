from aiogram.utils.callback_data import CallbackData

cb_order_action = CallbackData("order", "action")
cb_order_marketplace_action = CallbackData("order", "action", "marketplace","marketplace_id")
cb_order_pickup_point_action = CallbackData(
    "order", "action", "marketplace", "pickup_point_id"
)
