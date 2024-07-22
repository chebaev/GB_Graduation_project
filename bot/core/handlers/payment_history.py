from datetime import datetime

from aiogram import Bot
from aiogram.types import Message


import time
from core.database.core import crud
from core.database.common.models import Order
from core.settings.settings import settings
from core.utils.working_datetime import get_left_days_in_seconds



db_get_order = crud.get_order()


async def get_history(message: Message, bot: Bot):
    """
    Функция выводит платежи пользователей
    :param message:
    :param bot:
    :return:
    """
    telegram_id = message.from_user.id
    text = ''
    count = 0
    data = db_get_order(str(telegram_id))

    for elem in data:
        if elem.telegram_id == str(telegram_id):
            count += 1
            text += f'№ {count} | {str(elem.created_date)[:19]} | {elem.money} руб.\n'

    if text == '':
        text = 'Пока у Вас нет платежей'
    await bot.send_message(telegram_id, f'<b>История платежей</b>\n'
                                        f'{text}')
    await message.answer()