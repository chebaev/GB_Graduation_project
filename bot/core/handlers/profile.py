from aiogram import Bot
from aiogram.types import Message
from aiogram.fsm.context import FSMContext


from core.database.common.models import User
from core.database.core import crud

db_write = crud.adding_data()
db_filter = crud.get_filter_users()


async def get_profile(message: Message, bot: Bot):
    await bot.send_message(message.from_user.id,f'Описание подписки ')
