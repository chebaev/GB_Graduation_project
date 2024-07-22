import time
import datetime

from aiogram import Bot
from aiogram.types import Message, LabeledPrice, PreCheckoutQuery
from aiogram.types import CallbackQuery

from core.settings.settings import settings
from core.database.core import crud
from core.database.common.models import Order, User, UserReferrer, Attribute, AdminPanelTab
from datetime import datetime

from core.utils.site_api import site_api
from core.utils.working_datetime import days_to_seconds

db_all_data = crud.get_all_data()
db_write = crud.adding_data()
db_filter = crud.get_filter_users()
db_user_data = crud.get_data()
db_update = crud.update()
site_get_user = site_api.get_user_attribute()
site_set_user = site_api.set_user()



def get_amount(amount: int) -> int:
    """
    Функция просматривает по сумме сколько дней начислить пользователю
    :param amount:
    :return:
    """
    result = 0
    discount_1_months = 0
    discount_3_months = 0
    discount_6_months = 0
    discount_12_months = 0
    data_db = db_all_data(AdminPanelTab)
    for elem in data_db:
        price_day = elem.discount_price_day
        discount_1_months = ((settings.days_month * price_day) - (elem.discount_1_months * price_day))
        discount_3_months = ((settings.days_month * price_day)*3 - (elem.discount_3_months * price_day))
        discount_6_months = ((settings.days_month * price_day)*6 - (elem.discount_6_months * price_day))
        discount_12_months = ((settings.days_month * price_day)*12 - (elem.discount_12_months * price_day))
    if discount_1_months <= amount < discount_3_months:
        result = settings.days_month
    elif discount_3_months <= amount < discount_6_months:
        result = settings.days_month * 3
    elif discount_6_months <= amount < discount_12_months:
        result = settings.days_month * 6
    elif discount_12_months <= amount:
        result = settings.days_month * 12
    return result
def entry_to_the_database_order(money: float, telegram_id: str):
    """
    Добовление в базу данных Orders
    """
    data_order = {'telegram_id': telegram_id,
                   'money': money}
    db_write(Order, data_order)

def check_referrer(telegram_id: str):
    """
    Проверка реферрера в таблице UserReferrer если есть то добавляет в таблицу User
    :param telegram_id:
    :return:
    """
    if db_filter(UserReferrer, telegram_id):
        _referrer_id = db_user_data(UserReferrer, telegram_id, UserReferrer.referrer_id)
        uuid = db_user_data(User, _referrer_id, User.uuid)
        seconds_left = db_user_data(User, _referrer_id, User.seconds_left) + days_to_seconds(settings.referrer_day)

        enable = site_get_user(telegram_id=telegram_id, element='enable')
        _data = {
            'balance': db_user_data(User, _referrer_id, User.balance) + settings.referrer_money,
            'seconds_left': seconds_left
        }
        db_update(User, _referrer_id, _data)
        site_set_user(telegram_id=_referrer_id, uuid=uuid, enable=enable, expiryTime=seconds_left * 1000)

def entry_to_the_database_user(money: float, day: int, telegram_id: str): # РАБОТАЮ
    """
    Добавление в базу данных Users
    """
    data_user: dict
    _access_levels = db_user_data(User, telegram_id, User.access_levels)
    uuid = db_user_data(User, telegram_id, User.uuid)
    enable = site_get_user(telegram_id=telegram_id, element='enable')

    if _access_levels == Attribute.private:
        if db_user_data(User, telegram_id, User.seconds_left) == 0:
            seconds_left = db_user_data(User, telegram_id, User.stop_days_left) + days_to_seconds(day)
            data_user = {'balance': db_user_data(User, telegram_id, User.balance) + money,
                         'stop_days_left': seconds_left}
        else:
            seconds_left = db_user_data(User, telegram_id, User.seconds_left) + days_to_seconds(day)
            data_user = {'balance': db_user_data(User, telegram_id, User.balance) + money,
                         'seconds_left': seconds_left}
        site_set_user(telegram_id=telegram_id, uuid=uuid, enable=enable, expiryTime=seconds_left * 1000)

    elif _access_levels == Attribute.demo:
        check_referrer(telegram_id)
        seconds_left = int(time.time()) + days_to_seconds(day)
        data_user = {'access_levels': Attribute.private,
                     'balance': db_user_data(User, telegram_id, User.balance) + money,
                     'seconds_left': seconds_left,
                     'referral_link': f'https://t.me/{settings.bot_nickname}?start={telegram_id}',
                     'status': True}
        site_set_user(telegram_id=telegram_id, uuid=uuid, enable=True, expiryTime=seconds_left * 1000)
    return db_update(User, telegram_id, data_user)


async def process_pre_checkout_query(pre_checkout_query: PreCheckoutQuery, bot: Bot):
    """
    Срабатывает после получения оплаты
    Срабатывает когда пользователь нажал на кнопку Заплатить
    """
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)



async def successful_payment(message: Message):
    """
    Срабатывает когда пользователь оплатил услугу
    :param message:
    :return:
    """

    if message.successful_payment.invoice_payload == "add_balance":
        _money = message.successful_payment.total_amount / 100
        _telegram_id = str(message.from_user.id)
        _day = get_amount(int(_money))
        entry_to_the_database_order(money=_money, telegram_id=_telegram_id)
        entry_to_the_database_user(money=get_amount(int(_money)), day=_day, telegram_id=_telegram_id)

        msg = f'Спасибо за оплату {_money} {message.successful_payment.currency}.'
        await message.answer(msg)

def data_db(number:str):
    """
    Функция подсчёта денег включая скидку берется с базы данных
    :param number: берется с кнопки автоматически
    :return:
    """
    data_db = db_all_data(AdminPanelTab)
    for elem in data_db:
        result = 0
        price_day = elem.discount_price_day
        if number == '1':
            result = ((settings.days_month * price_day)-(elem.discount_1_months * price_day))
        elif number == '3':
            result = ((settings.days_month * 3 * price_day)-(elem.discount_3_months * price_day))
        elif number == '6':
            result = ((settings.days_month * 6 * price_day)-(elem.discount_6_months * price_day))
        elif number == '12':
            result = ((settings.days_month * 12 * price_day)-(elem.discount_12_months * price_day))
        return result



async def get_balans(callback: CallbackQuery, bot: Bot):
    """
    Функция оплаты
    :param callback:
    :param bot:
    :return:
    """
    code = callback.data[7:]
    money = data_db(code)
    msg = ''
    if code == '1':
        msg = f'Оплата за {code} месяц {money} ₽'
    elif code == '3':
        msg = f'Оплата за {code} месяца стоимость {money} ₽'
    elif code in ['6', '12']:
        msg = f'Оплата за {code} месяцев стоимость {money} ₽'


    await callback.bot.send_invoice(
        chat_id=callback.from_user.id,
        title='Пополнить баланс',
        description=f'{msg}',
        provider_token=settings.yootoken.get_secret_value(),
        payload='add_balance',
        currency='rub',
        prices=[
            LabeledPrice(
                label=f'Пополнить баланс на {money}',
                amount=(money * 100)
            )
        ],
        max_tip_amount=5000,
        suggested_tip_amounts=[1000, 2000, 3000, 4000],
        start_parameter=settings.bot_name,
        provider_data=None,
        need_name=False,
        need_phone_number=False,
        need_email=False,
        need_shipping_address=False,
        is_flexible=False,
        disable_notification=False,
        protect_content=False,
        reply_to_message_id=None,
        reply_markup=None,
        request_timeout=60
    )
    await callback.answer()
