from aiogram import Bot
from aiogram.types import  CallbackQuery
from core.keyboards.offer_keyboard import offer_inline
from core.utils.working_datetime import days_to_seconds, get_left_days_in_seconds
from core.database.common.models import User
from core.database.core import crud
from core.settings.settings import settings

db_filter = crud.get_filter_users()
db_user_day_second = crud.get_data()

async def public_offer(callback: CallbackQuery, bot: Bot):
    """
    Функция выводит сообщения Публичная оферта.
    :param callback:
    :param bot:
    :return:
    """
    telegram_id = callback.from_user.id
    if db_filter(User, telegram_id):
        if db_user_day_second(User, str(telegram_id), User.status) == True:
            result = get_left_days_in_seconds(db_user_day_second(User, str(telegram_id), User.seconds_left))
        else:
            result = get_left_days_in_seconds(db_user_day_second(User, str(telegram_id), User.stop_days_left))
        await bot.send_message(telegram_id, f'{callback.from_user.first_name}\n Вы уже зарегистрированы на сервисе\n'
                                            f'У Вас осталось {result}')

    else:
        await bot.send_message(telegram_id, text=f'<b>Публичная оферта.</b>\nПравила телеграм бота @{settings.bot_nickname}.\n'
                                             f'Ознакомится с информацией можно нажав на кнопку:\n '
                                                 f'« Открыть полный текст оферты »\n'
                                             f'<b>Если Вас всё устраивает нажмите на кнопку « Принять » </b>',
                               reply_markup=offer_inline)


