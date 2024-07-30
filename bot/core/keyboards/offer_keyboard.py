from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from core.settings.settings import settings



offer_inline = InlineKeyboardMarkup(inline_keyboard=[
    [
      InlineKeyboardButton(
          text='Открыть полный текст оферты',
          web_app=WebAppInfo(url=settings.offer_url)
      )
    ],
    [
        InlineKeyboardButton(
            text='Принять',
            callback_data='bt_ok'
        ),

        InlineKeyboardButton(
            text='Отмена',
            callback_data='bt_cancel'
        )
    ]
])

