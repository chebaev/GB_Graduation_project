from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from core.database.common.models import AdminPanelTab
from core.settings.settings import settings
from core.database.core import crud

db_all_data = crud.get_all_data()
db_write = crud.adding_data()
db_create_tables = crud.create_tables()
db_create_tables()
price_day = 0
discount_1_months = 0
discount_3_months = 0
discount_6_months = 0
discount_12_months = 0

def data_db():
    data_db = db_all_data(AdminPanelTab)
    global price_day
    global discount_1_months
    global discount_3_months
    global discount_6_months
    global discount_12_months
    for elem in data_db:
        price_day = elem.discount_price_day
        discount_1_months = elem.discount_1_months
        discount_3_months = elem.discount_3_months
        discount_6_months = elem.discount_6_months
        discount_12_months = elem.discount_12_months



def topay_inlinekb():
    data_db()
    topay_inlinekb_list = [
        [
            InlineKeyboardButton(
                text=f'Оплата за 1 месяц стоимость {((settings.days_month * price_day)-(discount_1_months * price_day))} ₽',
                callback_data='balans_1'
            )
        ],
        [
            InlineKeyboardButton(
                text=f'Оплата за 3 месяца стоимость '
                     f'{((settings.days_month * price_day)*3)-(discount_3_months * price_day)} ₽',
                callback_data='balans_3'
            )
        ],
        [
            InlineKeyboardButton(
                text=f'Оплата за 6 месяцев стоимость '
                     f'{((settings.days_month * price_day)*6)-(discount_6_months * price_day)} ₽',
                callback_data='balans_6'
            )
        ],
        [
            InlineKeyboardButton(
                text=f'Оплата за 12 месяцев стоимость '
                     f'{((settings.days_month * price_day)*12)-(discount_12_months * price_day)} ₽',
                callback_data='balans_12'
            )
        ],
        [
            InlineKeyboardButton(
                text='🏠 Главное меню',
                callback_data='bt_main_menu'
            )
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=topay_inlinekb_list)