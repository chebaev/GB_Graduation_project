import io
import os
import qrcode

from aiogram import Bot
from aiogram.types import Message, CallbackQuery, FSInputFile

from core.database.common.models import User, Order
from core.database.core import crud
from core.keyboards.main_menu_inline import main_menu_inline, main_menu_connect_inline

db_user_data = crud.get_data()
db_filter = crud.get_filter_users()


def qr_code(link: str):

    img = qrcode.make(link)

    # Если нужно сохранить в памяти
    io_data = io.BytesIO()
    img.save(io_data, 'png')
    return io_data.getvalue()

async def get_link_connect(message: Message, bot: Bot):
    telegram_id = message.from_user.id
    if db_filter(User, str(telegram_id)):
        if db_user_data(User, str(telegram_id), User.status):
            await bot.send_message(telegram_id, f'<b>Ваша ссылка для подключения, скопируйте её и вставьте в приложение по инструкции:</b>')
            await bot.send_message(telegram_id,f'{db_user_data(User, telegram_id, User.connect_link)}',
                                   reply_markup=main_menu_connect_inline)
        else:
            await bot.send_message(telegram_id,f'<b>Ваш профиль не активный. Возможные причины:</b>\n'
                                               f'- активна приостановка использования\n'
                                               f'- недостаточно средств на счету.\n')
            await bot.send_message(telegram_id,f'{db_user_data(User, telegram_id, User.connect_link)}',
                                   reply_markup=main_menu_connect_inline)
    await message.answer()

async def get_qr_connect(callback: CallbackQuery, bot: Bot):
    telegram_id = str(callback.from_user.id)
    if db_filter(User, telegram_id):
        if db_user_data(User, telegram_id, User.status):
            data = db_user_data(User, telegram_id, User.connect_link)

            path = f'core/file/code_{telegram_id}.png'

            img = qrcode.make(data)
            img.save(path)
            photo = FSInputFile(path)
            await callback.message.answer_photo(caption='Ваш QR-код для подключения', photo=photo,
                                                reply_markup=main_menu_connect_inline)
            try:
                os.remove(path)
            except FileNotFoundError:
                pass


        else:
            await bot.send_message(int(telegram_id), f'<b>Ваш профиль не активный. Возможные причины:</b>\n'
                                                     f'- активна приостановка использования\n'
                                                     f'- недостаточно средств на счету.\n')
            await bot.send_message(telegram_id,f'{db_user_data(User, telegram_id, User.connect_link)}',
                                   reply_markup=main_menu_connect_inline)
    await callback.answer()


