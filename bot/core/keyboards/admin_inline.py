from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

admin_inline = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(
            text='Работа с пользователями  ->',
            callback_data='working_user'
        )
    ],
    [
        InlineKeyboardButton(
            text='Изменить данные в БД ->',
            callback_data='change_bd'
        )
    ],
    [
        InlineKeyboardButton(
            text='Сколько пользователей в БД',
            callback_data='all_user'
        )
    ],
    [
        InlineKeyboardButton(
            text='Выручка за месяц',
            callback_data='revenue_month'
        )
    ],
    [
        InlineKeyboardButton(
            text='Выручка за период',
            callback_data='period_revenue'
        )
    ]
])

end_date_inline = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(
            text='Выберите дату конечную',
            callback_data='end_date'
        )
    ]
])

working_admin_inline = InlineKeyboardMarkup(inline_keyboard=[
[
        InlineKeyboardButton(
            text='Проверка пользователя',
            callback_data='user_verification'
        )
    ],
    [
        InlineKeyboardButton(
            text='Добавить время работы',
            callback_data='hours_add_working'
        )
    ],
    [
        InlineKeyboardButton(
            text='Отправить сообщение всем',
            callback_data='send_message_all'
        )
    ],
    [
        InlineKeyboardButton(
            text='🏠 Предыдущее меню',
            callback_data='admin_panel'
        )
    ]
])

сhecking_message_inline = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(
            text='Отправить',
            callback_data='message_send'
        ),

        InlineKeyboardButton(
            text='Отмена',
            callback_data='cancel_message'
        )
    ]
    ])

change_inline = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(
            text='Поменять демо доступ (днях)',
            callback_data='discount_demo'
        )
        ],
    [
        InlineKeyboardButton(
            text='Поменять цену за день',
            callback_data='discount_day'
        )
    ],
    [
        InlineKeyboardButton(
            text='Скидка за 1 месяц (днях)',
            callback_data='discount_1'
        )
    ],
    [
        InlineKeyboardButton(
            text='Скидка за 3 месяц (днях)',
            callback_data='discount_3'
        )
    ],
    [
        InlineKeyboardButton(
            text='Скидка за 6 месяц (днях)',
            callback_data='discount_6'
        )
    ],
    [
        InlineKeyboardButton(
            text='Скидка за 12 месяц (днях)',
            callback_data='discount_12'
        )
    ],
    [
        InlineKeyboardButton(
            text='Сообщение о скидках',
            callback_data='discount_message'
        )
    ],
    [
        InlineKeyboardButton(
            text='🏠 Предыдущее меню',
            callback_data='admin_panel'
        )
    ]
])