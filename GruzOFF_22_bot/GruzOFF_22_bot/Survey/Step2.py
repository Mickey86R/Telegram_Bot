from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup

from aiogram.utils.markdown import text

from Survey.Survey  import Survey
from Survey.Survey  import SurveyForAdmin
from Modules import Repository
from Keyboards import PayingFromUser

# Здесь будет обработка подтверждения администратором заявки и отправка соответствующего сообщения пользователю


# Received confirm from admin, sending messages about payment
async def confirm_received_from_admin(call: types.CallbackQuery, state: FSMContext):
    await edit_message_after_confirm_and_send_messages(call, state)
    

# Edit message after confirm/decline/edit and send messages to admin and user (user_state: waiting_confirm)
async def edit_message_after_confirm_and_send_messages(call: types.CallbackQuery, state: FSMContext):

    data = call.data.split('_')[1]

    
    app_id = get_app_id_from_text_message(call.message.text)
    user_id = Repository.get_user_id_from_number_app(app_id)

    await call.message.bot.edit_message_reply_markup(
                                    chat_id = call.from_user.id,
                                    message_id = call.message.message_id, 
                                    reply_markup = None)

    if data == 'Confirm':
        
        await call.message.bot.send_message(
                                        chat_id = user_id,
                                        text = text(f"Ваш номер заявки: {app_id}",
                                                    f"Для размещения в группе Вы можете внести символическую плату администратору канала (номер карты сбера: 2202206142454607) или же опубликовать заявку бесплатно.",
                                                    sep = "\n"),
                                        reply_markup = PayingFromUser.to_pay_keyboard)


    elif data == 'Decline':
        await call.message.bot.send_message(
                                        chat_id = user_id,
                                        text = "Ваша заявка отклонена")

    elif data == 'Edit':
        await call.message.answer("Напишите, что необходимо исправить пользователю")
        await state.set_state(SurveyForAdmin.waiting_edit.state)
        print(f"USER_ID: {user_id}")
        await state.update_data(user_id = user_id)


# Received pay message, send message to admin for confirm
async def edit_from_admin(message: types.Message, state: FSMContext):
    
    user_data = await state.get_data()
    user_id = user_data.get("user_id")
    await state.finish()

    text_edit = f"Ваша заявка не прошла одобрение, администротор рекомендует Вам отредактировать следующие пункты:\n {message.text}"

    await message.bot.send_message(user_id, text_edit)
    await message.answer("Отправлено!")
        


# Get application_id from text_message
def get_app_id_from_text_message(text):
    print(f'параметр в функции get_app_id_from_text_message: {text}')
    number = text.split()[2]
    print(f'Полученный номер заявки: {number}')
    return number

    
def register_handlers_survey_step_2(dp: Dispatcher):

    dp.register_callback_query_handler(confirm_received_from_admin, Text(startswith = 'AdminChoise_'), state = "*")
    dp.register_message_handler(edit_from_admin, state = SurveyForAdmin.waiting_edit)

    
