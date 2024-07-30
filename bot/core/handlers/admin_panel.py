import time
from typing import Any

from aiogram import Bot
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram_calendar import get_user_locale

from core.keyboards.admin_inline import admin_inline, end_date_inline, working_admin_inline, сhecking_message_inline, \
    change_inline
from core.database.core import crud
from core.database.common.models import User, AdminPanelTab
from aiogram_calendar import SimpleCalendar

from datetime import datetime

from core.state.state_date import StateUser, StateVerification, AdminPanel, AdminPanel_BD
from core.utils.site_api import site_api
from core.utils.working_datetime import days_to_seconds, get_left_days_in_seconds

db_get_how_many_users = crud.get_how_many_users()
db_get_monthly_report = crud.get_monthly_report()
db_get_report_for_period = crud.get_report_for_period()
db_get_columns_data = crud.get_data()
db_filter = crud.get_filter_users()
db_update = crud.update()
db_get_all_data = crud.get_all_data()
db_get_user_check = crud.get_user_check()
site_get_user = site_api.get_user_attribute()
site_set_user = site_api.set_user()
db_all_data = crud.get_all_data()
db_update_adminpanel = crud.update_adminpanel()

from core.settings.settings import settings

async def hours_add_working(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.message.answer("Введите Telegram_id пользователя:")
    await state.set_state(StateUser.user_telegram_id)


async def user_telegram_id(message: Message, bot: Bot, state: FSMContext):
    flag = True
    while flag:
        user_telegram_id = message.text
        if db_filter(User, user_telegram_id):
            await state.update_data(user_telegram_id=message.text)
            await bot.send_message(message.from_user.id, "Введите на сколько дней увеличить:")
            await state.set_state(StateUser.user_days)
            flag = False
        else:
            await bot.send_message(message.from_user.id, f"Ошибка!!! Вы ввели не правильный id или "
                                                         f"такого нет в базе данных")
            await state.set_state(StateUser.user_telegram_id)
            flag = False


async def user_days(message: Message, bot:Bot, state: FSMContext):
    """
    Добавление дней пользователю в днях
    """
    flag = True
    while flag:
        number = message.text
        if number.isdigit():
            data = await state.get_data()
            telegram_id = data.get("user_telegram_id")
            if db_filter(User, telegram_id):
                await bot.send_message(message.from_user.id, f"Вы вели telegram_id: {telegram_id}\n"
                                                             f" Добавить дней: {number}")
                seconds_left = db_get_columns_data(User, telegram_id, User.seconds_left)
                if seconds_left == 0:
                    seconds_left = int(time.time()) + days_to_seconds(int(number))
                else:
                    seconds_left = seconds_left + days_to_seconds(int(number))

                uuid = db_get_columns_data(User, telegram_id, User.uuid)
                data = {
                    'seconds_left': seconds_left,
                    'status': True
                }
                db_update(User, telegram_id, data)
                enable = True #site_get_user(telegram_id=telegram_id, element='enable')
                site_set_user(telegram_id=telegram_id, uuid=uuid, enable=enable, expiryTime=seconds_left * 1000)

                await bot.send_message(message.from_user.id, f'Время увеличено для telegram_id: {telegram_id} \n'
                                                             f'Сейчас у него {get_left_days_in_seconds(
                                                                 db_get_columns_data(User, telegram_id,
                                                                                     User.seconds_left))}')
            else:
                await bot.send_message(message.from_user.id, f"Пользователя с таким telegram_id = '{telegram_id}"
                                                             f"' <b>Нет.</b>\n"
                                                             f"Может быть вы ошиблись")
            await state.clear()
            flag = False
        else:
            await bot.send_message(message.from_user.id, f"Вы ошиблись. Введите число")
            await state.set_state(StateUser.user_days)
            break




async def get_user_verification(message: Message, bot: Bot, state: FSMContext):
    await bot.send_message(message.from_user.id, f'Проверка пользователя.\n'
                                                 f'Введите telegram_id для проверки:')
    await state.set_state(StateVerification.user_telegram_id)


async def state_user_verification(message: Message, bot: Bot, state: FSMContext):
    user_telegram_id = message.text
    if db_filter(User, user_telegram_id):
        data = db_get_user_check(user_telegram_id)

        for elem in data:
            await bot.send_message(message.from_user.id, f'telegram_id = {user_telegram_id}\n'
                                                         f'Статус ={elem.status}\n'
                                                         f'Уровни доступа = {elem.access_levels}\n'
                                                         f'Дней = {get_left_days_in_seconds(elem.seconds_left)}')
    else:
        await bot.send_message(message.from_user.id, f'такого пользователя нет БД. ({user_telegram_id})')
    await state.clear()

async def get_working_admin(callback_query:CallbackQuery):
    await callback_query.message.delete()
    await callback_query.message.answer(f'Работа с пользователями', reply_markup=working_admin_inline)





async def get_admin(message: Message, bot: Bot):

    user = str(message.from_user.id)
    if user in settings.admins_id_group:
        await bot.send_message(user,f'Добро пожаловать {message.from_user.first_name}\n'
                                    f'Админ панель', reply_markup=admin_inline)

async def get_all_user(message: Message, bot: Bot):
    """
    Функция обработки кнопки -> 'Сколько пользователей в БД'
    :param message:
    :param bot:
    :return:
    """
    await bot.send_message(message.from_user.id, f'На текущей момент пользователей = {db_get_how_many_users(User)}')
    await message.answer()

async def get_revenue_month(message: Message, bot: Bot):
    """
    Функция обработки кнопки -> 'Выручка за месяц'
    :param message:
    :param bot:
    :return:
    """
    money = db_get_monthly_report()
    if money == None:
        await bot.send_message(message.from_user.id, f'Выручка за месяц = 0 руб.')
    else:
        await bot.send_message(message.from_user.id, f'Выручка за месяц = {money} руб.')
    await message.answer()

# Выручка за период'

async def get_period_revenue(callback_query: CallbackQuery):
    """
    Функция обработки кнопки -> 'Выручка за период'
    :param message:
    :param bot:
    :return:
    """
    # await callback_query.message.answer("Выберите дату начала: ",
    #                        reply_markup=await SimpleCalendar(
    #                            locale=await get_user_locale(callback_query.from_user)).start_calendar()
    await callback_query.message.answer("Выберите дату начала: ",
                                        reply_markup=await SimpleCalendar().start_calendar()
    )
    await callback_query.message.delete()

async def state_end_date(callback_query: CallbackQuery, state: FSMContext):
    state_data = await state.get_data()
    end_date = state_data.get('end_date')
    if not end_date:
        await callback_query.message.answer(
                               f"Выберите дату конечную :",
                               reply_markup=await SimpleCalendar().start_calendar()
                               )

        await callback_query.message.delete()
async def process_simple_calendar(callback_query: CallbackQuery, callback_data: CallbackData, state: FSMContext):
    calendar = SimpleCalendar(
        locale=await get_user_locale(callback_query.from_user), show_alerts=True
    )
    calendar.set_dates_range(datetime(2024, 1, 1), datetime(2045, 12, 31))
    selected, date = await calendar.process_selection(callback_query, callback_data)
    if selected:
        _date = date.strftime("%Y-%m-%d")

        state_data = await state.get_data()
        start_date = state_data.get('start_date')
        if start_date == None:
            await state.update_data(start_date=_date)
            await callback_query.message.answer(
                f'Вы выбрали {_date}', reply_markup=end_date_inline
            )
            await callback_query.answer()

        else:
            await state.update_data(end_date=_date)
            summa = db_get_report_for_period(start_date, _date)
            if summa == None:
                await callback_query.message.answer(f'За период с {start_date} до {_date}\n'
                                                    f'Не было оплат')
            else:
                await callback_query.message.answer(f'За период с {start_date} до {_date}\n'
                                                f'Сумма = {summa} руб.')

            await state.clear()



#**************************************************
async def send_message_all(message: Message, bot: Bot, state: FSMContext):
    await bot.send_message(message.from_user.id,"Введите сообщение оно отправится всем пользователям:")
    await state.set_state(AdminPanel.user_message)


async def user_message_admin(message: Message, bot: Bot, state: FSMContext):
    await state.update_data(user_message=message.text)
    await bot.send_message(message.from_user.id, f"<b>Ваше сообщение:</b>\n"
                                                 f"{message.text}",
                                                    reply_markup=сhecking_message_inline)

async def message_send(callback_query: CallbackQuery, bot: Bot, state: FSMContext):
    await callback_query.message.delete()
    data = await state.get_data()
    user_message = data.get('user_message')
    db_data = db_get_all_data(User)
    telegram_id = 0
    for elem in db_data:
       telegram_id = int(elem.telegram_id)
       await bot.send_message(telegram_id, f"{user_message}")
    # await callback_query.message.answer(f'Сообщение отправлено {user_message}')
    await state.clear()

async def cancel_message_admin(callback_query: CallbackQuery, bot: Bot, state: FSMContext):
    await callback_query.message.delete()
    data = await state.get_data()
    user_message = data.get('user_message')
    await callback_query.message.answer(f"Сообщение не было отправлено {user_message}",
                                        reply_markup=working_admin_inline)

    await state.clear()

#**************************************************

async def change_bd(callback_query: CallbackQuery):
    await callback_query.message.answer(f"Выберите что хотите изменить",
                           reply_markup=change_inline)

async def processing_discounts(callback_query: CallbackQuery, state: FSMContext):
    name = callback_query.data
    await state.update_data(name=name)

    await callback_query.message.answer(f"Введите значение:")
    await state.set_state(AdminPanel_BD.receive_message)

async def receive_message(message: Message,bot: Bot, state: FSMContext):
    result = {}
    data = await state.get_data()
    value = data.get('name')
    name = value[9:]
    discount_price_day = 0
    discount_1_months = 0
    discount_3_months = 0
    discount_6_months = 0
    discount_12_months = 0
    discount_message = ''

    data_db = db_all_data(AdminPanelTab)
    for elem in data_db:
        discount_price_day = elem.discount_price_day
        discount_demo_day = elem.discount_demo_day
        discount_message = elem.discount_message
        discount_1_months = elem.discount_1_months
        discount_3_months = elem.discount_3_months
        discount_6_months = elem.discount_6_months
        discount_12_months = elem.discount_12_months

    pattern = ['1', '3', '6', '12', 'day', 'demo']
    if name in pattern:
        number = message.text
        if number.isdigit():
            if name == 'demo':
                await bot.send_message(message.from_user.id, f"Поменять {discount_demo_day} дней на {message.text} дней.")
                result = {'discount_demo_day': int(message.text)}
            elif name == 'day':
                await bot.send_message(message.from_user.id, f"Поменять {discount_price_day} руб. на {float(message.text)} руб.")
                result = {'discount_price_day': float(message.text)}
            elif name == '1':
                await bot.send_message(message.from_user.id, f"Поменять {discount_1_months} руб. на {message.text} руб.")
                result = {'discount_1_months': int(message.text)}
            elif name == '3':
                await bot.send_message(message.from_user.id, f"Поменять {discount_3_months} руб. на {message.text} руб.")
                result = {'discount_3_months': int(message.text)}
            elif name == '6':
                await bot.send_message(message.from_user.id, f"Поменять {discount_6_months} руб. на {message.text} руб.")
                result = {'discount_6_months': int(message.text)}
            elif name == '12':
                await bot.send_message(message.from_user.id, f"Поменять {discount_12_months} руб. на {message.text} руб.")
                result = {'discount_12_months': int(message.text)}
        else:
            await bot.send_message(message.from_user.id, f'Вы ввели не число.\n'
                                                         f'Повторите ещё раз')
            await state.set_state(AdminPanel_BD.receive_message)
    elif name == 'message':
        await bot.send_message(message.from_user.id, f"Вы ввели {message.text}. Было: {discount_message}")
        result = {'discount_message': message.text}
    db_update_adminpanel(result)








