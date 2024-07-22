from aiogram import Bot
from aiogram.types import Message

from core.database.common.models import User, Attribute
from core.database.core import crud
from core.keyboards.register_inline import register_inline

db_user_data = crud.get_data()
db_filter = crud.get_filter_users()

async def user_invite_friend(message: Message, bot: Bot):
    telegram_id = message.from_user.id
    if db_filter(User, str(telegram_id)):
        if db_user_data(User, str(telegram_id), User.access_levels) == Attribute.demo:
            await bot.send_message(telegram_id, f'<b>Вы ещё ни разу не оплатили сервис.</b>\n'
                                                f'После оплаты ссылка появится автоматически')
        else:
            await bot.send_message(telegram_id,f'<b>Пошлите другу ссылку:</b>\n\n'
                                               f'{db_user_data(User, str(telegram_id), User.referral_link)}\n\n'
                                               f' Когда ваш друг зайдет в наш бот по этой ссылке создаст аккаунт\n'
                                               f' и оплатит первый месяц, вы получите <b>+ 15 дней</b>'
                                               f' пользования нашим сервисом!')
    else:
        await bot.send_message(telegram_id, f'😊 Здравствуйте {message.from_user.first_name} к сожалению.\n'
                                            f'<b>Вы ещё не зарегистрировались.</b>\n'
                                            f'После регистрации и оплаты ссылка появится автоматически',
                               reply_markup=register_inline)


