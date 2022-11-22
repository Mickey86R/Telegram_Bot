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
from Keyboards import MainMenuButton
from Keyboards import SetDayInlineMenu
from Keyboards import SetChoiseWithApplication
from Keyboards import YesOrNo
from Keyboards import PayingFromUser

# Здесь будет происходить обработка подтверждения админом оплаты


# Подтверждение платежа от пользователя
async def confirm_payment_from_admin(call: types.CallbackQuery):
    print('input in confirm_payment_from_admin')
    await call.bot.edit_message_reply_markup(
                                            chat_id = call.from_user.id,
                                            message_id = call.message.message_id, 
                                            reply_markup = None)
    
    
    if call.data == 'Payment_ok':
        
        number_app = get_app_id_from_text_message(call.message.text)
        app = Repository.get_app(number_app)
        username = get_username_from_text_message(call.message.text)

        text_app = make_application_to_group(app, username)
        await call.message.bot.send_message(chat_id = config.chat_id, text = text_app)
    
    elif call.data == 'Payment_no':

        number_app = get_app_id_from_text_message(call.message.text)
        print(f'Номер заявки: {number_app}')
        app = Repository.get_app(number_app)
        await call.message.bot.send_message(chat_id = app.from_user, text = "Вы не оплатили. Заполните заявку ещё раз.")



# Get application_id from text_message
def get_app_id_from_text_message(text):
    print(f'параметр в функции get_app_id_from_text_message: {text}')
    number = text.split()[2]
    print(f'Полученный номер заявки: {number}')
    return number


def get_username_from_text_message(text):
    name = text.split()[4]
    print(f'Полученный username: {name}')
    return name


# Make application text for send to admin to confirm
def make_kpacuBo(number_app, user_name, user_data: FSMContext):
    
    application = text(f'Номер заявки: {number_app}',
                        f'Пользователь: @{user_name}',
                        f'{user_data.get("day")}',
                        f'Требуется: {user_data.get("humans")} человек',
                        f'Адрес: {user_data.get("address")}',
                        f'Время: {user_data.get("time")}',
                        f'Задача: {user_data.get("task")}',
                        f'Оплата: {user_data.get("pay")}',
                        sep = "\n")
    return application


# Make application text for send to group
def make_application_to_group(app:Repository.Application, user_name):
    
    application = text(f'{app.day}',
                        f'Пользователь: {user_name}',
                        f'Требуется: {app.humans} человек',
                        f'Адрес: {app.address}',
                        f'Время: {app.time}',
                        f'Задача: {app.task}',
                        f'Оплата: {app.pay}',
                        sep = "\n")
    return application




    
def register_handlers_survey_step_4(dp: Dispatcher):

    dp.register_callback_query_handler(confirm_payment_from_admin, Text(startswith = 'Payment_'))

    