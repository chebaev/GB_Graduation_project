from aiogram import Bot
from aiogram.types import Message, CallbackQuery, FSInputFile

from core.keyboards.register_inline import register_inline
from core.keyboards.profile_inline import profile_inline_blocked, profile_inline_active

from core.utils.working_datetime import get_left_days_in_seconds
from core.settings.settings import settings
from core.database.common.models import User, UserReferrer, AdminPanelTab
from core.database.core import crud

db_filter_user = crud.get_filter_users()
db_user_day_second = crud.get_data()
db_write = crud.adding_data()
db_user_data = crud.get_data()
db_check_data = crud.get_all_data()

def get_referrer(telegram_id: str, referrer_id:str):
    """
    Функция отвечает за проверку реферальной подписки
    :param telegram_id:
    :param referrer_id:
    :return:
    """

    if referrer_id != '' and not db_filter_user(UserReferrer, telegram_id):
        data = {'telegram_id': telegram_id,
                 'referrer_id': referrer_id}
        db_write(UserReferrer, data)

async def get_start(message: Message, bot: Bot):
    """
    Функция запускается при старте бота
    :param message:
    :param bot:
    :return:
    """
    demo_day = 0
    price_day = 0
    discount_message = ' '
    referrer_id = message.text[7:]
    telegram_id = str(message.from_user.id)

    get_referrer(telegram_id, referrer_id)



    if db_filter_user(User, telegram_id):
        if db_user_data(User, telegram_id, User.status):
            keyboard = profile_inline_active
        else:
            keyboard = profile_inline_blocked
        await bot.send_message(message.from_user.id, f'Здравствуйте {message.from_user.first_name}!\n\n'
                                                     f'<b>У Вас осталась {get_left_days_in_seconds(db_user_day_second(User, telegram_id, User.seconds_left))}</b>\n\n'
                                                     f'Если Вы потеряли настройки, можете повторно их скачать,\n'
                                                     f'нажав на кнопку "Получить ссылку"\n\n'
                                                     f'<a href="{settings.url_news}">Новости проекта</a>\n\n'
                                                     f'👭 Пригласите друзей в наш сервис и получите +15 дней за каждого друга '
                                                     f'(если друг произведет оплату).',
                               reply_markup=keyboard)

    else:
        path = f'core/file/logo.png'
        photo = FSInputFile(path)
        await bot.send_photo(chat_id=message.chat.id, photo=photo)
        demo_day = 0
        price_day = 0
        for elem in db_check_data(AdminPanelTab):
            demo_day = elem.discount_demo_day
            price_day = elem.discount_price_day
            discount_message = elem.discount_message

        await bot.send_message(int(telegram_id),
                               f'😊 Здравствуйте! Рад вас видеть, {message.from_user.first_name}\n'
                               f'{f"\n<b>{discount_message}</b>\n" if discount_message != " " else ''}'
                               f'Я - безопасный и надежный бот, который поможет вам всегда быть на связи с миром: \n'
                               f'- устойчив к блокировкам\n'
                               f'- у меня высокая скорость \n'
                               f'- обеспечу доступ ко всем сайтам\n'
                               f'- можно оплатить картами РФ \n'
                               f'- есть возможность приостановить использование сервиса с сохранением баланса\n\n'
                               f'<b>Моя стоимость всего {price_day} руб. в день!</b>\n\n'
                               
                               f'Также вы можете отслеживать свою статистику в днях\n\n'
                               f'👭 Пригласите друзей и получите +15 дней за каждого друга'
                               f' (если друг произведет оплату).\n'
                               f'Проверьте меня – пользуйтесь {demo_day} дней совершенно бесплатно!'
                               , reply_markup=register_inline)


async def get_start_inline(callback: CallbackQuery, bot: Bot):

    telegram_id = callback.from_user.id
    if db_filter_user(User, str(telegram_id)):
        if db_user_data(User, str(telegram_id), User.status):
            keyboard = profile_inline_active
        else:
            keyboard = profile_inline_blocked
        await bot.send_message(telegram_id, f'Здравствуйте {callback.from_user.first_name}!\n\n'
                                                     f'<b>У Вас осталась {get_left_days_in_seconds(
                                                         db_user_day_second(User, str(telegram_id),
                                                                            User.seconds_left))}</b>\n\n'
                                                     f'Если Вы потеряли настройки, можете повторно их скачать,\n'
                                                     f'нажав на кнопку "Получить ссылку"\n\n'
                                                     f'👭 Пригласите друзей в наш сервис и получите +15 дней за каждого друга '
                                                     f'(если друг произведет оплату).',
                               reply_markup=keyboard)

    else:
        discount_message = ''
        demo_day = 0
        price_day = 0
        for elem in db_check_data(AdminPanelTab):
            demo_day = elem.discount_demo_day
            price_day = elem.discount_price_day
            discount_message = elem.discount_message
        await bot.send_message(telegram_id,
                               f'😊 Здравствуйте! Рад вас видеть, {callback.from_user.first_name}\n'
                               f'{f"\n<b>{discount_message}</b>\n" if discount_message != " " else ''}'
                               f'Я - безопасный и надежный бот, который поможет вам всегда быть на связи с миром: \n'
                               f'- устойчив к блокировкам\n'
                               f'- у меня высокая скорость \n'
                               f'- обеспечу доступ ко всем сайтам\n'
                               f'- можно оплатить картами РФ \n'
                               f'- есть возможность приостановить использование сервиса с сохранением баланса\n\n'
                               f'<b>Моя стоимость всего {price_day} руб. в день!</b>\n\n'
                               
                               f'Также вы можете отслеживать свою статистику в днях\n\n'
                               f'👭 Пригласите друзей и получите +15 дней за каждого друга'
                               f' (если друг произведет оплату).\n'
                               f'Проверьте меня – пользуйтесь {demo_day} дней совершенно бесплатно!',
                               reply_markup=register_inline)
    await callback.answer()