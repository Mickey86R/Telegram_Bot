import config

from aiogram import Dispatcher, types
from aiogram.dispatcher.filters import Text

async def check_follow(bot, user_id):
    user_channel_status = await bot.get_chat_member(chat_id = config.chat_id, user_id = user_id)
    if user_channel_status["status"] != "left":
        return True
    else:
        return False
