import config
import asyncio
import logging

from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher.filters import Text
from aiogram.utils.markdown import text
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from Modules import OtherHandlers
from Modules import MyFSM
from Modules.OtherHandlers import register_other_handlers
from Modules.MyFSM import register_handlers_survey
from Modules.CheckFollow import check_follow
from Keyboards.MyCommands import set_commands
from Survey.StepsBeforeConfirming import register_handlers_survey_before_confirming 
from Survey.Step2 import register_handlers_survey_step_2
from Survey.Step3 import register_handlers_survey_step_3
from Survey.Step4 import register_handlers_survey_step_4

# Logging On, for dismiss new messages
logging.basicConfig(level = logging.INFO)
logger = logging.getLogger(__name__)

global bot

async def check(user_id):
    return await check_follow(bot, user_id)

# Start polling new objects
async def main():

    # Настройка логирования в stdout
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )
    logger.error("Starting bot")

    # Объявление и инициализация объектов бота и диспетчера
    bot = Bot(token = config.token)
    dp = Dispatcher(bot, storage = MemoryStorage())

    # Регистрация хэндлеров
    register_other_handlers(dp)
    register_handlers_survey_before_confirming(dp)
    register_handlers_survey_step_2(dp)
    register_handlers_survey_step_3(dp)
    register_handlers_survey_step_4(dp)
    #register_handlers_survey(dp)

    # Установка команд бота
    await set_commands(bot)

    # Запуск поллинга
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())