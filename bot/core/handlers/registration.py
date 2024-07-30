import time
from loguru import logger
from uuid import uuid4
from aiogram import Bot
from aiogram.types import CallbackQuery


from core.keyboards.profile_inline import profile_inline_active
from core.utils.working_datetime import days_to_seconds
from core.database.common.models import User, AdminPanelTab
from core.database.core import crud
from core.utils.site_api import site_api



con_link = site_api.connection_link()
site_user_add = site_api.add_user()
db_write = crud.adding_data()
db_filter = crud.get_filter_users()
db_all_data = crud.get_all_data()

def proverka_adminpanel():
    if not db_all_data(AdminPanelTab):
        data = {
            'discount_demo_day': 7,
            'discount_price_day': 2
        }
        db_write(AdminPanelTab, data)
async def start_register(callback: CallbackQuery, bot: Bot):
    """
    При нажатии на копку 'ОК'
    :param message:
    :param state:
    :return:
    """
    demo_day = [elem.discount_demo_day for elem in db_all_data(AdminPanelTab)][0]
    telegram_id = callback.from_user.id
    if db_filter(User, str(telegram_id)):
        await bot.send_message(telegram_id, f'{callback.from_user.first_name}\n Вы уже зарегистрированы')
    else:

        await bot.send_message(telegram_id,f'⭐️ Регистрация успешна ⭐️\n\n' 
                                           f'Пробный период предоставлен на {demo_day * 24} часов\n\n'
                                           f'Далее необходимо нажать на кнопку <b>Получить ссылку</b>,'
                                           f' затем <b>Инструкции по установке</b>',
                               reply_markup=profile_inline_active)
        seconds_time = int(time.time()) + days_to_seconds(demo_day)
        uuid = str(uuid4())
        link = con_link(telegram_id, uuid)
        data = {'telegram_id': telegram_id,
                 'uuid': uuid,
                 'first_name': callback.from_user.first_name,
                 'username': callback.from_user.username,
                 'seconds_left': seconds_time,
                 'connect_link': link}
        db_write(User, data)
        code = site_user_add(telegram_id=str(telegram_id), uuid=uuid, expiryTime=(seconds_time * 1000))
        if code == 404:
            logger.error(f'Проблема с подключением к службе XRAX. Нового пользователя {telegram_id} нельзя добавить ')
        else:
            logger.info(f'Успешно добавлен новый пользователь {telegram_id}')
        await callback.message.delete()


