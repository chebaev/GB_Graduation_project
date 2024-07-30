from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

keyboard_support = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(
            text='Ответить без сохранения',
            callback_data='bt_support'
        )
    ],
    [
        InlineKeyboardButton(
            text="Ответить с сохранением в БД",
            callback_data='save_support'
        )
    ]
])

keyboard_support_not_save = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(
            text='Ответить пользователю',
            callback_data='bt_support'
        )
    ]
])