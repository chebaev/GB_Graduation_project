import time
from datetime import datetime
from aiogram import Bot
from core.settings.settings import settings

from core.database.common.models import User, UserReferrer, Attribute
from core.database.core import crud
from core.utils.working_datetime import get_left_days_in_seconds

db_update = crud.update()

db_get_user_shutdown = crud.get_user_shutdown()
db_get_before_shutdown = crud.get_before_shutdown()

async def check_days_until_shutdown(bot: Bot):
    """
    Проверка сколько дней осталось до отключения
    :return:
    """
    data = db_get_before_shutdown()
    for elem in data:
        if elem.status and (elem.access_levels == Attribute.private):
            if (elem.before_shutdown > 0) and (elem.seconds_left - int(time.time()) == elem.before_shutdown) :
                await bot.send_message(elem.telegram_id, f"У Вас осталось {elem.before_shutdown} дней.\n"
                                                         f"Пополните баланс и продолжите пользоваться нашим VPN сервисом")
                data = {
                    'before_shutdown': elem.before_shutdown - 1,

                }
                db_update(User, elem.telegram_id, data)

async def check_once_month(bot: Bot):
    data = db_get_before_shutdown()
    for elem in data:
        if not elem.status and (elem.access_levels == Attribute.private):
            if elem.before_shutdown == 0:
                await bot.send_message(elem.telegram_id, f"Вы давно не заходили.\n"
                                                         f"Пополните баланс и продолжите пользоваться нашим VPN")


    # (elem.seconds_left - int(time.time()) == elem.before_shutdown):


async def database_check_for_shutdown():
    """
    Проверка в базе данных пользователей у кого вышло оплаченное время каждый час
    :return:
    """
    data = db_get_user_shutdown()
    for elem in data:
        if elem.status and (elem.seconds_left - int(time.time()) <= 0):
            data = {
                'status': False,
                'seconds_left': 0
            }
            db_update(User, elem.telegram_id, data)
