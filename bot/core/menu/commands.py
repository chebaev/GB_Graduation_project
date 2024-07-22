from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault


async def set_commands(bot: Bot):
    commands = [
        BotCommand(
            command='start',
            description='🏠 Главное меню'
        ),
        BotCommand(
            command='topay',
            description='💸 Пополнить баланс'
        ),
        BotCommand(
            command='invite',
            description='🤝 Пригласить друга'
        ),
        BotCommand(
            command='help',
            description='🆘 Помощь в работе'
        )
    ]

    await bot.set_my_commands(commands, BotCommandScopeDefault())