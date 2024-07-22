from aiogram import Bot
from aiogram.types import Message
from core.keyboards.help_inline import help_inline, hellp_vpn_inline, chat_support_inline
from core.settings.settings import settings
from core.database.core import crud

db_user_data = crud.get_data()
db_filter = crud.get_filter_users()

async def get_help(message: Message, bot: Bot):
    telegram_id = message.from_user.id
    await bot.send_message(telegram_id, f'<b>Выберите тему для получения помощи:</b>\n',
                           reply_markup=help_inline)

async def get_vpn_not_work(message: Message, bot: Bot):
    telegram_id = message.from_user.id
    await bot.send_message(telegram_id,f'❗ ️Если не устанавливается соединение:\n'
                                       f'- посмотрите сколько дней осталось (Главное меню);\n'
                                       f'- переустановите приложение с очисткой данных;\n'
                                       f'- проверьте, что Вы не приостановили использование сервисом '
                                       f'(Главное меню -> Возобновить использование)\n'
                                       f'- проверьте, что выключены другие аналогичные программы и сервисы, если такие имеются.\n\n'
                                       f'❗️ Низкая скорость:\n'
                                       f'Попробуйте перезагрузить телефон или включить\выключить'
                                       f' режим самолета, чтобы обновить регистрацию на базовой станции.\n\n'
                                       f'Если Вы уверены, что проблема не в этом, напишите нам в "Чат поддержки".',
                           reply_markup=hellp_vpn_inline)
    await message.answer()

async def get_chat_support(message: Message, bot: Bot):
    await bot.send_message(message.from_user.id, f"️ ️❗️ Прежде чем обращаться в службу поддержки,\n"
                                                 f"загляните в раздел Помощь, возможно там вы найдете ответ на свой вопрос.\n\n"
                                                 f"<a href='{settings.url_support}'>Чат поддержки</a>",
                           reply_markup=chat_support_inline)
    await message.answer()


async def get_payments(message: Message, bot: Bot):
    await bot.send_message(message.from_user.id, f'В редких случаях оплата может не пройти.\n'
                                                 f'В таком случае попробуйте еще раз\n'
                                                 f'(получите новую платежную ссылку), или попробуйте\n'
                                                 f'произвести оплату другим способом.',
                           reply_markup=hellp_vpn_inline)
    await message.answer()

