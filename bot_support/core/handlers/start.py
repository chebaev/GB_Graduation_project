from aiogram import Bot
from aiogram.types import Message
from loguru import logger

from ..settings.settings import settings



@logger.catch
async def get_start(message: Message, bot: Bot):
    """
    Функция срабатывает при первоначальном старте
    :param message:
    :param bot:
    :return:
    """

    await bot.send_message(chat_id=message.from_user.id, text=f'<b>Вы попали в тех.поддержку {settings.bot_name}</b>.\n\n'
                                                              f'Опишите свою проблему, мы поможем Вам!')
