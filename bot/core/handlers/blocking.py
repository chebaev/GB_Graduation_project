import time
from aiogram import Bot
from aiogram.types import Message, CallbackQuery
from core.database.common.models import Attribute

from core.database.common.models import User
from core.database.core import crud

from core.handlers.start import db_user_day_second
from core.keyboards.profile_inline import profile_inline_blocked, profile_inline_active
from core.utils.working_datetime import days_to_seconds, get_left_days_in_seconds
from core.utils.site_api import site_api

db_filter = crud.get_filter_users()
db_time_check = crud.get_time_check()
db_update = crud.update()
update_site = site_api.set_user()

db_user_data = crud.get_data()


async def user_temporary_blocking(callback: CallbackQuery, bot: Bot):
    """
    Функция отвечает за блокировку пользователя
    :param callback:
    :param bot:
    :return:
    """
    telegram_id = str(callback.from_user.id)
    time_check = db_time_check(User, telegram_id)
    text = (f'Здравствуйте {callback.from_user.first_name}!\n\n'
           f'<b>У Вас осталась {get_left_days_in_seconds(db_user_day_second(User, telegram_id, User.seconds_left))}</b>\n\n'
           f'Если Вы потеряли настройки, можете повторно их скачать,\n'
           f'нажав на кнопку "Получить ссылку"\n\n'
           f'👭 Пригласите друзей в наш сервис и получите +15 дней за каждого друга. '
           f'(Если друг оплатит месяц.)')

    if callback.data == 'button_suspend_use' and not time_check:

        if db_user_data(User, telegram_id, User.access_levels) in [Attribute.private, Attribute.admin]:
            await callback.message.edit_text(text)
            await callback.message.edit_reply_markup(reply_markup=profile_inline_blocked)
            await callback.answer(f'Минимальный период приостановки - 24 часа', show_alert=True)
            balances_by_time = db_user_data(User, telegram_id, User.seconds_left) - int(time.time())
            data = {'status': False,
                    'blocking_user': int(time.time()) + days_to_seconds(1), # Указать нужно days_to_seconds(1)
                    'stop_days_left': balances_by_time,
                    'seconds_left': 0}

            db_update(User, telegram_id, data)
            uuid = db_user_data(User, telegram_id, User.uuid)
            update_site(telegram_id=telegram_id, uuid=uuid, enable=False)

        else:
            await bot.send_message(int(telegram_id), f'В <b>пробном периоде</b> приостановка использования недоступна.\n'
                                                f'После оплаты всё будет работать')

    elif callback.data == "button_resume_use":

        seconds = db_user_data(User, telegram_id, User.blocking_user)
        summa_seconds = seconds - int(time.time())
        if summa_seconds > 0:
            await callback.answer(f"Ваш аккаунт заблокирован на время {get_left_days_in_seconds(seconds)}\n\n"
                                   f"После истечения времени можно 'Возобновить использование'", show_alert=True)
        else:
            await callback.answer(f'Ваш аккаунт разблокирован\n', show_alert=True)
            await callback.message.edit_reply_markup(reply_markup=profile_inline_active)
            seconds_left = int(time.time()) + db_user_data(User, telegram_id, User.stop_days_left)
            uuid = db_user_data(User, telegram_id, User.uuid)

            data = {'status': True,
                    'blocking_user': 0,
                    'seconds_left': seconds_left,
                    'stop_days_left': 0}
            db_update(User, telegram_id, data)
            update_site(telegram_id=telegram_id, uuid=uuid, enable=True, expiryTime=seconds_left*1000)

    await callback.answer()


