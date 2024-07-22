from aiogram import Bot
from aiogram.types import Message

from core.keyboards.register_inline import register_inline
from core.keyboards.topay_inline import topay_inlinekb
from core.database.common.models import User
from core.database.core import crud
from core.utils.working_datetime import get_left_days_in_seconds
from core.utils.utils import get_status

db_filter = crud.get_filter_users()
db_user_data = crud.get_data()



async def get_topay(message: Message, bot: Bot):
    telegram_id = str(message.from_user.id)
    if db_filter(User, telegram_id):
        _datetime = get_left_days_in_seconds(db_user_data(User, telegram_id, User.seconds_left))
        await bot.send_message(message.from_user.id, f'Здравствуйте {message.from_user.first_name}!\n'
                                                     f'<b>У Вас осталось {_datetime},'
                                                     f' аккаунт {get_status(telegram_id=telegram_id)} </b>\n\n'
                                                     f'<b>На текущий момент оплата производится через сервис ЮKassa. </b>\n\n',

                               reply_markup=topay_inlinekb())

    else:
        await bot.send_message(message.from_user.id,
                               f'😊 Здравствуйте {message.from_user.first_name} к сожалению.\n'
                               f' Вы ещё не зарегистрированы.\n\n',
                                reply_markup=register_inline)