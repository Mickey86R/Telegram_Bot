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

from Modules import CheckFollow
from Modules import Repository
from Keyboards import MainMenuButton
from Keyboards import SetDayInlineMenu
from Keyboards import SetChoiseWithApplication
from Keyboards import YesOrNo
from Keyboards import PayingFromUser

class Survey(StatesGroup):
    waiting_day = State()
    waiting_humans = State()
    waiting_address = State()
    waiting_time = State()
    waiting_task = State()
    waiting_pay = State()
    waiting_confirm = State()
    waiting_payment_confirm = State()

    
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
    await message.answer('Опишите задачу.')


# Received task message, send payment message
async def task_received(message: types.Message, state: FSMContext):
    
    await state.update_data(task = message.text)
    await state.set_state(Survey.waiting_pay.state)
    await message.answer('Сколько Вы готовы заплатить за данную работу?')
    

# Received pay message, send message to admin for confirm
async def pay_received(message: types.Message, state: FSMContext):
    
    await state.update_data(pay = str(message.text))
    await state.set_state(Survey.waiting_confirm.state)

    number_app = await add_application_in_db(message, state)
    text_application = make_kpacuBo(number_app, message.from_user.username, await state.get_data())

    await message.bot.send_message(int(config.owners_id[2]), text_application, reply_markup = SetChoiseWithApplication.setChoise_keyboard)
    await message.answer("Заявка на одобрении. После одобрения заявки Вам придёт счёт на оплату.\nРекомендуем не нажимать кнопку 'Главное меню', т.к. это приведёт к отмене заявки. Спасибо за ожидание!")


# Received confirm from admin, user must send screenshot
async def confirm_received(message: types.Message, state: FSMContext):
    print('input in confirm_received')
    if(message.content_type == 'photo'):
        print('snter in photo')
        await state.set_state(Survey.waiting_payment_confirm.state)

        await message.forward(chat_id = config.owners_id[2])
        print('пересылка сообщения')

        number_app = Repository.get_last_app_from_user_id(message.from_user.id)

        await message.bot.send_message(
                                       chat_id = config.owners_id[2], 
                                       text = text(f"Заявка номер: {number_app}",
                                                   f"От: @{message.from_user.username}",
                                                   "Одобряем?", sep = "\n"), 
                                       reply_markup = YesOrNo.setChoise_keyboard)
        print("отправка в чат")


    number_app = await add_application_in_db(message, state)
    text_application = make_kpacuBo(number_app, message.from_user.username, await state.get_data())


# Received confirm from admin, sending messages about payment
async def confirm_received_from_admin(call: types.CallbackQuery):
    await edit_message_after_confirm_and_send_messages(call)
    

# Edit message after confirm/decline/edit and send messages to admin and user (user_state: waiting_confirm)
async def edit_message_after_confirm_and_send_messages(call: types.CallbackQuery):

    data = call.data.split('_')[1]

    if data == 'Confirm':
        
        await call.message.bot.edit_message_reply_markup(
                                    chat_id = call.from_user.id,
                                    message_id = call.message.message_id, 
                                    reply_markup = None)
        
        app_id = get_app_id_from_text_message(call.message.text)
        user_id = Repository.get_user_id_from_number_app(app_id)        
        
        await call.message.bot.send_message(
                                        chat_id = user_id,
                                        text = f"Ваш номер заявки: {app_id}\nДля размещения в группе необходимо призвести оплату.",
                                        reply_markup = PayingFromUser.to_pay_keyboard)


    elif data == 'Decline':
        await call.message.bot.send_message(
                                        chat_id = user_id,
                                        text = "Ваша заявка отклонена")

    elif data == 'Edit':
        return 


# Get application_id from text_message
def get_app_id_from_text_message(text):
    print(f'параметр в функции get_app_id_from_text_message: {text}')
    number = text.split()[2]
    print(f'Полученный номер заявки: {number}')
    return number


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
def make_application_to_group(app:Repository.Application):
    
    application = text(f'{app.day}',
                        f'Требуется: {app.humans} человек',
                        f'Адрес: {app.address}',
                        f'Время: {app.time}',
                        f'Задача: {app.task}',
                        f'Оплата: {app.pay}',
                        sep = "\n")
    return application


# Add aplication in DB
async def add_application_in_db(message: types.Message, state: FSMContext):
    
    user_data = await state.get_data()

    now = datetime.now() 
    current_time = now.strftime("%Y%m%d%H%M%S") 
    
    Repository.new_app(current_time, message.from_user.id, user_data)
    return current_time


async def payment_from_user(call: types.CallbackQuery, state = FSMContext):
    print('input in payment_from_user')
    await call.bot.edit_message_text(
                                     chat_id = call.from_user.id,
                                     message_id = call.message.message_id, 
                                     text = call.message.text,
                                     reply_markup=None)
    print('call get_last_app_from_user_id')

    def get_number_app(text):
        print(f'параметр в функции get_app_id_from_text_message: {text}')
        number = text.split()[3]
        print(f'Полученный номер заявки: {number}')
        return number

    application = Repository.get_app(get_number_app(call.message.text))
    print('call make kpacubo')
    text_app = make_application_to_group(application)
    await call.message.bot.send_message(chat_id = config.chat_id, text = f"Заказчик: @{call.from_user.username}\n{text_app}")


# Подтверждение платежа от пользователя
async def confirm_payment_from_admin(call: types.CallbackQuery):
    print('input in confirm_payment_from_admin')
    await call.bot.edit_message_reply_markup(
                                            chat_id = call.from_user.id,
                                            message_id = call.message.message_id, 
                                            reply_markup=None)
    
    number_app = get_app_id_from_text_message(call.message.text)
    print('Номер заявки: {number_app}')
    if call.data == 'Payment_ok':
        app = Repository.get_app(number_app)
        text_app = make_application_to_group(app)
        await call.message.bot.send_message(chat_id = config.chat_id, text = text_app)
    
def register_handlers_survey(dp: Dispatcher):

    dp.register_message_handler(start_survey, Text(equals = "Составить заявку"), state='*')
    dp.register_callback_query_handler(day_received, Text(startswith = 'Give_'), state = Survey.waiting_day)
    dp.register_message_handler(humans_received, state = Survey.waiting_humans)
    dp.register_message_handler(address_received, state = Survey.waiting_address)
    dp.register_message_handler(time_received, state = Survey.waiting_time)
    dp.register_message_handler(task_received, state = Survey.waiting_task)
    dp.register_message_handler(pay_received, state = Survey.waiting_pay)
    dp.register_callback_query_handler(confirm_received_from_admin, Text(startswith = 'AdminChoise_'))
    dp.register_callback_query_handler(payment_from_user, Text(equals = "Paying"), state = Survey.waiting_confirm)
    dp.register_message_handler(confirm_received, content_types = ['photo'], state = Survey.waiting_confirm)
    dp.register_callback_query_handler(confirm_payment_from_admin, Text(startswith = 'Payment_'))
    dp.register_callback_query_handler(confirm_received_from_admin, Text(startswith = 'AdminChoise_'))

    