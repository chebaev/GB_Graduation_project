from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

profile_inline_active = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(
            text='🪙 Пополнить баланс',
            callback_data='bt_balans'
        )
    ],
    [
        InlineKeyboardButton(
            text='Получить ссылку',
            callback_data='link_connect_bt'
        )
    ],
    [
        InlineKeyboardButton(
            text='Получить QR-код',
            callback_data='link_qr_bt'
        )
    ],
    [
        InlineKeyboardButton(
            text='📑 История платежей',
            callback_data='histore_order_bt'
        )
    ],
    [
        InlineKeyboardButton(
            text='❄️ Приостановить использование',
            callback_data='button_suspend_use'
        )
    ],
    [
        InlineKeyboardButton(
            text='👬 Пригласить друга',
            callback_data='invite_friend_bt'
        ),
        InlineKeyboardButton(
            text='🆘 Помощь',
            callback_data='help_bt'
        )

    ]
])

profile_inline_blocked = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(
            text='💸 Пополнить баланс',
            callback_data='bt_balans'
        )
    ],
    [
        InlineKeyboardButton(
            text='Получить ссылку',
            callback_data='link_connect_bt'
        )
    ],
    [
        InlineKeyboardButton(
            text='📑 История платежей',
            callback_data='histore_order_bt'
        )
    ],
    [
        InlineKeyboardButton(
            text='Возобновить использование',
            callback_data='button_resume_use'
        )
    ],
    [
        InlineKeyboardButton(
            text='👬 Пригласить друга',
            callback_data='invite_friend_bt'
        ),
        InlineKeyboardButton(
            text='🆘 Помощь',
            callback_data='help_bt'
        ),
    ]
])