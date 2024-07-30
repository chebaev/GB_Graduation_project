from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from core.settings.settings import settings



help_inline = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(
            text='🛠 Инструкции по установке',
            # callback_data='bt_Installation_Instructions'
            web_app=WebAppInfo(url=settings.hellp_url)
        )
    ],
    [
        InlineKeyboardButton(
            text='Проблемы с подключением',
            callback_data='bt_vpn_not_work'
        )
    ],
    [
        InlineKeyboardButton(
            text='💸 Платежи',
            callback_data='payments_bt'
        )
    ],
    [
        InlineKeyboardButton(
            text='🏠 Главное меню',
            callback_data='bt_main_menu'
        )
    ]
])

hellp_vpn_inline = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(
            text='💬 Чат поддержки',
            callback_data='chat_support'
        )
    ],
    [
        InlineKeyboardButton(
            text='🏠 Предыдущее меню',
            callback_data='help_bt'
        )
    ]
    ])
chat_support_inline = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(
            text='🏠 Предыдущее меню',
            callback_data='bt_vpn_not_work'
        )
    ]
])