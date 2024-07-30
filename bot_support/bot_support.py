import asyncio
# import logging
from loguru import logger
from aiogram import Bot, Dispatcher, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import Command

from core.handlers.start import get_start
from core.handlers.support import get_wait_message, reply_to_user, state_admin, RegAnswer, reply_to_user_save
from core.menu.commands import set_commands
from core.settings.settings import settings
from core.database.core import crud

db_create_tables = crud.create_tables()


async def start_bot(bot: Bot):
    await bot.send_message(settings.admin_id.get_secret_value(), text='Бот запущен')
    logger.info('Бот запущен')

async def stop_bot(bot: Bot):
    await bot.send_message(settings.admin_id.get_secret_value(), text='Бот остановлен')
    logger.info('Бот остановлен')
@logger.catch
async def start():
    db_create_tables()

    bot = Bot(token=settings.token.get_secret_value(), default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()

    dp.startup.register(start_bot)
    dp.shutdown.register(stop_bot)
    dp.message.register(get_start, Command(commands='start'))
    dp.callback_query.register(reply_to_user, F.data.startswith('bt_support'))
    dp.callback_query.register(reply_to_user_save, F.data.startswith('save_support'))
    dp.message.register(state_admin, RegAnswer.answer)
    dp.message.register(get_wait_message)

    await set_commands(bot)

    try:
        await dp.start_polling(bot, skip_update=True)
    finally:
        await bot.session.close()
        logger.exception("When the bot starts: ")

if __name__ == '__main__':
    logger.add('logs/logs.log', format='{time} {level} {message}', level='DEBUG',
               rotation='30 days', compression="zip")
    asyncio.run(start())