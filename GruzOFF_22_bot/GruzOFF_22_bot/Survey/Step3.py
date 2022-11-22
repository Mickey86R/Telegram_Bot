import config

from yookassa import Configuration,Payment

from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup

from Keyboards import SetDayInlineMenu
from Modules import CheckFollow

from aiogram.utils.markdown import text

from emoji import emojize

from datetime import datetime

from Survey.Survey import Survey
from Modules import CheckFollow
from Modules import Repository
from Keyboards import SetDayInlineMenu
from Keyboards import YesOrNo

# Здесь будет происходить обработка нажатия кнопки оплатить или скриншота от клиента и отправка соответствующего сообщения админу


#
async def user_paying(call: types.CallbackQuery, state: FSMContext):
    
    await call.message.bot.edit_message_reply_markup(
                                    chat_id = call.from_user.id,
                                    message_id = call.message.message_id, 
                                    reply_markup = None)

    number_app = get_app_id_from_text_message(call.message.text)
    app = Repository.get_app(number_app)
    text_app = make_application_to_group(app, call.from_user.username)

    await call.message.bot.send_message(chat_id = config.chat_id, text = text_app)
    # pay_process
      
 

# Received confirm from admin, user must send screenshot
async def confirm_received(message: types.Message, state: FSMContext):
    print('input in confirm_received')
    print('snter in photo')
    await state.finish()

    await message.forward(chat_id = config.owners_id[2])
    print('пересылка сообщения')

    number_app = Repository.get_last_app_from_user_id(message.from_user.id)

    await message.bot.send_message(
                                   chat_id = config.owners_id[2], 
                                   text = text(f"Заявка номер: {number_app}",
                                               f"От: @{message.from_user.username}",
                                               "Одобряем?", sep = "\n"), 
                                   reply_markup = YesOrNo.setChoise_keyboard)
    print("отправка админу")


# Get application_id from text_message
def get_app_id_from_text_message(text):
    number = text.split()[3]
    return number


# Make application text for send to group
def make_application_to_group(app:Repository.Application, user_name):
    
    application = text(f'{app.day}',
                        f'Пользователь: @{user_name}',
                        f'Требуется: {app.humans} человек',
                        f'Адрес: {app.address}',
                        f'Время: {app.time}',
                        f'Задача: {app.task}',
                        f'Оплата: {app.pay}',
                        sep = "\n")
    return application


def register_handlers_survey_step_3(dp: Dispatcher):

    dp.register_message_handler(confirm_received, content_types = ['photo'], state = Survey.waiting_confirm)
    dp.register_callback_query_handler(user_paying, Text(startswith = 'Paying'), state = Survey.waiting_confirm)
    
    