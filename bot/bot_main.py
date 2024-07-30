import asyncio
from loguru import logger
import os
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from datetime import datetime

from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram_calendar import SimpleCalendarCallback

from core.database.core import crud

from core.handlers.admin_panel import get_admin, get_all_user, get_revenue_month, get_period_revenue, \
    process_simple_calendar, state_end_date, get_working_admin, user_telegram_id, hours_add_working, user_days, \
    get_user_verification, state_user_verification, send_message_all, user_message_admin, message_send, \
    cancel_message_admin, change_bd, processing_discounts, receive_message
from core.handlers.blocking import user_temporary_blocking
from core.handlers.help import get_help, get_vpn_not_work, get_chat_support, get_payments
from core.handlers.invite_friend import user_invite_friend
from core.handlers.link_connect import get_link_connect, get_qr_connect

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from core.handlers.public_offer import public_offer
from core.state.state_date import StateUser, StateVerification, AdminPanel, AdminPanel_BD
from core.utils.polling_database_time import database_check_for_shutdown, check_days_until_shutdown, check_once_month

from core.settings.settings import settings
from core.menu.commands import set_commands
from core.handlers.start import get_start, get_start_inline
from core.handlers.registration import start_register, proverka_adminpanel
from core.handlers.order_ykassa import get_balans, process_pre_checkout_query, successful_payment
from core.handlers.topay import get_topay
from core.handlers.profile import get_profile
from core.handlers.payment_history import get_history

db_create_tables = crud.create_tables()
db_write = crud.adding_data()
db_all_data = crud.get_all_data()
db_set_admin_panel = crud.set_admin_panel()

async def start_bot(bot: Bot):
    await bot.send_message(settings.admin_id.get_secret_value(), text=f'Бот запущен {datetime.now()}')
    logger.info('Bot start')

async def stop_bot(bot: Bot):
    await bot.send_message(settings.admin_id.get_secret_value(), text=f'Бот остановлен {datetime.now()}')
    logger.info('Bot stop')


async def start():
    db_create_tables()
    data = {
        'id': 1,
        'discount_demo_day': 7,
        'discount_price_day': 2,
        'discount_message': '',
        'discount_1_months': 0,
        'discount_3_months': 10,
        'discount_6_months': 20,
        'discount_12_months': 30
    }
    db_set_admin_panel(data)


    bot = Bot(token=settings.token.get_secret_value(), default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()

    # ------------ Работа бота по таймеру
    scheduler = AsyncIOScheduler()
    scheduler.add_job(check_once_month, trigger='cron',day=10, hour=10, minute=30, kwargs={'bot': bot})
    scheduler.add_job(check_days_until_shutdown, trigger='cron', hour=14, minute=30, kwargs={'bot': bot})
    scheduler.add_job(database_check_for_shutdown, trigger='interval', minutes=(settings.polling_time))
    # -----------------------------------
    scheduler.start()

    dp.startup.register(start_bot)
    dp.shutdown.register(stop_bot)
    dp.message.register(get_start, Command(commands='start'))
    dp.message.register(get_topay, Command(commands='topay'))
    dp.message.register(get_profile, Command(commands='profile'))
    dp.message.register(user_invite_friend, Command(commands='invite'))
    dp.message.register(get_help, Command(commands='help'))
    dp.message.register(get_admin, Command(commands='admin'))

    # Регистрация handlers
    dp.callback_query.register(public_offer, F.data.startswith('bt_register'))
    dp.callback_query.register(start_register, F.data.startswith('bt_ok'))
    dp.callback_query.register(get_start_inline, F.data.startswith('bt_cancel'))

    dp.callback_query.register(get_history, F.data.startswith('histore_order_bt'))
    dp.callback_query.register(user_temporary_blocking, F.data.startswith('button_'))
    dp.callback_query.register(user_invite_friend, F.data.startswith('invite_friend_bt'))
    dp.callback_query.register(get_link_connect, F.data.startswith('link_connect_bt'))
    dp.callback_query.register(get_qr_connect, F.data.startswith('link_qr_bt'))
    dp.callback_query.register(get_help, F.data.startswith('help_bt'))
    dp.callback_query.register(get_vpn_not_work, F.data.startswith('bt_vpn_not_work'))
    dp.callback_query.register(get_start_inline, F.data.startswith('bt_main_menu'))
    dp.callback_query.register(get_chat_support, F.data.startswith('chat_support'))
    dp.callback_query.register(get_payments, F.data.startswith('payments_bt'))

    # ****************** Админ панель *************

    dp.callback_query.register(get_admin, F.data.startswith('admin_panel'))
    dp.callback_query.register(get_working_admin, F.data.startswith('working_user'))
    dp.callback_query.register(hours_add_working, F.data.startswith('hours_add_working'))
    dp.message.register(user_telegram_id, StateUser.user_telegram_id)
    dp.message.register(user_days, StateUser.user_days)
    dp.callback_query.register(get_user_verification, F.data.startswith('user_verification'))
    dp.message.register(state_user_verification, StateVerification.user_telegram_id)
    dp.callback_query.register(send_message_all, F.data.startswith('send_message_all'))
    dp.message.register(user_message_admin, AdminPanel.user_message)
    dp.callback_query.register(message_send, F.data.startswith('message_send'))
    dp.callback_query.register(cancel_message_admin, F.data.startswith('cancel_message'))
    dp.callback_query.register(change_bd, F.data.startswith('change_bd'))
    dp.callback_query.register(processing_discounts, F.data.startswith('discount_'))
    dp.message.register(receive_message, AdminPanel_BD.receive_message)

    # **********************************************

    dp.callback_query.register(get_all_user, F.data.startswith('all_user'))
    dp.callback_query.register(get_revenue_month, F.data.startswith('revenue_month'))
    dp.callback_query.register(get_period_revenue, F.data.startswith('period_revenue'))

    dp.callback_query.register(get_balans, F.data.startswith('balans_'))
    dp.callback_query.register(get_topay, F.data.startswith('bt_balans'))
    dp.callback_query.register(process_simple_calendar, SimpleCalendarCallback.filter())
    dp.callback_query.register(state_end_date, F.data.startswith('end_date'))
    dp.pre_checkout_query.register(process_pre_checkout_query)
    dp.message.register(successful_payment, F.successful_payment)
    await set_commands(bot)

    try:
        await dp.start_polling(bot, skip_updates=False)
    finally:
        await bot.session.close()

if __name__ == '__main__':
    logger.add('core/logs/logs.log', format='{time} {level} {message}', level='DEBUG',
               rotation='30 days', compression="zip")

    asyncio.run(start())