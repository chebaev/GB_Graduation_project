from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

register_inline = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(
            text='Зарегистрироваться на сервисе',
            callback_data='bt_register'
        )
    ]
])

