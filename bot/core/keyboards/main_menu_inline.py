
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo

from core.settings.settings import settings

main_menu_inline = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(
            text='🏠 Главное меню',
            callback_data='bt_main_menu'
        )
    ]
])

main_menu_connect_inline = InlineKeyboardMarkup(inline_keyboard=[
[
    InlineKeyboardButton(
        text='🛠 Инструкции по установке',
        # callback_data='bt_Installation_Instructions'
        web_app=WebAppInfo(url=settings.hellp_url)
    )
],
    [
        InlineKeyboardButton(
            text='🏠 Главное меню',
            callback_data='bt_main_menu'
        )
    ]
])