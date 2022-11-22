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

from Survey.Survey  import Survey
from Modules import CheckFollow
from Modules import Repository
from Keyboards import MainMenuButton
from Keyboards import SetDayInlineMenu
from Keyboards import SetChoiseWithApplication

#Здесь происходит опрос пользователя, и заканчивается на отправке сообщения администратору с просьбой подтвердить заявку

    
# Start Survey after click "Составить заявку"
async def start_survey(message: types.Message, state: FSMContext):
    
    if await CheckFollow.check_follow(message.bot, message.from_user.id):
        
        await message.answer(text('''Вы перешли в режим составления заявки.
Вы в любой момент можете прервать составление, нажав на кнопку "Главное меню"'''), 
                                reply_markup = MainMenuButton.mainMenu_Keyboard)
        await message.answer('Когда Вам нужны работники?', reply_markup = SetDayInlineMenu.setDay_keyboard)
        await state.set_state(Survey.waiting_day.state)


# Received day message, edit inline keyboard and send humans message
async def day_received(call: types.CallbackQuery, state: FSMContext):

    day = call.data.split("_")[1]

    async def my_func():
        if day == 'Now':
            return await edit_message_after_choise_day(call, 'Сейчас')

        elif day == 'Today':
            return await edit_message_after_choise_day(call, 'Сегодня')

        elif day == 'Tomorrow':
            return await edit_message_after_choise_day(call, 'Завтра')

    day = await my_func()
    
    await state.update_data(day = day)
    await state.set_state(Survey.waiting_humans.state)
    await call.message.answer('Сколько Вам нужно человек? (Введите число)')


# Delete inlinekeyboard and edit message
async def edit_message_after_choise_day(call, message):
    
    my_text = emojize(text('\N{double exclamation mark}', message, '\N{double exclamation mark}'))
    await call.message.bot.edit_message_text(
                chat_id = call.from_user.id,
                message_id = call.message.message_id, 
                text = my_text,
                reply_markup=None
            )
    return my_text


# Received humans message, send address message
async def humans_received(message: types.Message, state: FSMContext):

    await state.update_data(humans = str(message.text))
    await state.set_state(Survey.waiting_address.state)
    await message.answer('Укажите адрес, по которому будет происходить работа. (Включая подъезд и квартиру)')


# Received address message, send time message
async def address_received(message: types.Message, state: FSMContext):
    
    await state.update_data(address = message.text)
    await state.set_state(Survey.waiting_time.state)
    await message.answer('Укажите время, к которму Вам нужны работники. (формат времени - 24 часа)')


# Received time message, send task message
async def time_received(message: types.Message, state: FSMContext):
    
    await state.update_data(time = message.text)
    await state.set_state(Survey.waiting_task.state)
    await message.answer('Опишите задачу. (Вид работы, примерное время выполнения, объемы, этажи, и т.д.)')


# Received task message, send payment message
async def task_received(message: types.Message, state: FSMContext):
    
    await state.update_data(task = message.text)
    await state.set_state(Survey.waiting_pay.state)
    await message.answer('Сколько Вы готовы заплатить за данную работу? (Сумма / Минимальное количество часов / Процент / Карта или наличные)')
    

# Received pay message, send message to admin for confirm
async def pay_received(message: types.Message, state: FSMContext):
    
    await state.update_data(pay = str(message.text))
    await state.set_state(Survey.waiting_confirm.state)

    number_app = await add_application_in_db(message, state)
    text_application = make_kpacuBo(number_app, message.from_user.username, await state.get_data())

    await message.bot.send_message(int(config.owners_id[2]), text_application, reply_markup = SetChoiseWithApplication.setChoise_keyboard)
    await message.answer("Заявка на одобрении. После одобрения заявки Вам придёт счёт на оплату.\nРекомендуем не нажимать кнопку 'Главное меню', т.к. это приведёт к отмене заявки. Спасибо за ожидание!")


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


# Add aplication in DB
async def add_application_in_db(message: types.Message, state: FSMContext):
    
    user_data = await state.get_data()

    now = datetime.now() 
    current_time = now.strftime("%Y%m%d%H%M%S") 
    
    Repository.new_app(current_time, message.from_user.id, user_data)
    return current_time


def register_handlers_survey_before_confirming(dp: Dispatcher):

    dp.register_message_handler(start_survey, Text(equals = "Составить заявку"), state = '*')
    dp.register_callback_query_handler(day_received, Text(startswith = 'Give_'), state = Survey.waiting_day)
    dp.register_message_handler(humans_received, state = Survey.waiting_humans)
    dp.register_message_handler(address_received, state = Survey.waiting_address)
    dp.register_message_handler(time_received, state = Survey.waiting_time)
    dp.register_message_handler(task_received, state = Survey.waiting_task)
    dp.register_message_handler(pay_received, state = Survey.waiting_pay)
        