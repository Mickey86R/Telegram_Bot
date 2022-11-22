from aiogram import Bot
from aiogram.types import BotCommand

async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="/start", description="Старт бота, приветствие"),
        BotCommand(command="/help", description="Мне нужна помощь"),
    ]
    await bot.set_my_commands(commands)
