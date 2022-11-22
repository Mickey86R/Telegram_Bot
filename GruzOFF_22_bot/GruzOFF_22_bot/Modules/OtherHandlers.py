from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.utils.markdown import text


from Texts import CheckFollowMessages
from Texts import MainMenuMessage
from Texts import RulesOfMakingApplicationMessage
from Texts import RulesForExecutorsMessage
from Texts import OrderCommercialMessage
from Texts import InviteMessage
from Texts import ContactInformationMessage
from Modules import CheckFollow
from Modules import Repository
from Modules import MyFSM
from Keyboards import MainMenuButton
from Keyboards import MenuKeyBoard
from Keyboards import SetDayInlineMenu

# Handler to command /start
async def cmd_start(message: types.Message):
    #await message.answer(StartMessage.startMessage)

    if await CheckFollow.check_follow(message.bot, message.from_user.id):
        await message.answer(CheckFollowMessages.isFollow, reply_markup = MainMenuButton.mainMenu_Keyboard)
        print(message.from_id, message.from_user.username, message.text, "check_ok")
        Repository.new_or_update_user(message.from_id, True)
    else: 
        await message.answer(CheckFollowMessages.isNotFollow, reply_markup = types.ReplyKeyboardRemove())
        print(message.from_id, message.from_user.username, message.text, "check_not_ok")
        Repository.new_or_update_user(message.from_id, False)
    

# Handler to command /help
async def cmd_help(message: types.Message):
    await message.answer(ContactInformationMessage.message)


# Handler to keyboard "Главное меню"
async def kb_mainMenuWithoutState(message: types.Message):
    if await CheckFollow.check_follow(message.bot, message.from_user.id):
        await message.answer(MainMenuMessage.message, reply_markup = MenuKeyBoard.menuKeyboard)
        
        
# Handler to keyboard "Главное меню"
async def kb_mainMenuWithState(message: types.Message, state: FSMContext):
    await message.answer(MainMenuMessage.message, reply_markup = MenuKeyBoard.menuKeyboard)
    await state.finish()


# Handler to keyboard "Правила составления заявки"
async def kb_rules_of_application(message: types.Message):
    if await CheckFollow.check_follow(message.bot, message.from_user.id):
        await message.answer(RulesOfMakingApplicationMessage.message)


# Handler to keyboard "Правила для исполнителей"
async def kb_rules_for_executors(message: types.Message):
    if await CheckFollow.check_follow(message.bot, message.from_user.id):
        await message.answer(RulesForExecutorsMessage.message)


# Handler to keyboard "Заказать рекламу в канале"
async def kb_order_commercial(message: types.Message):
    if await CheckFollow.check_follow(message.bot, message.from_user.id):
        await message.answer(OrderCommercialMessage.message)


# Handler to keyboard "Составить заявку"
async def kb_make_application(message: types.Message):
    if await CheckFollow.check_follow(message.bot, message.from_user.id):
        
        await message.answer(text('''Вы перешли в режим составления заявки.
Вы в любой момент можете прервать составление, нажав на кнопку "Главное меню"'''), 
                                reply_markup = MainMenuButton.mainMenu_Keyboard)
        await message.answer('Когда Вам нужны работники?', reply_markup = SetDayInlineMenu.setDay_keyboard)


# Handler to keyboard "Пригласить человека в канал"
async def kb_invite(message: types.Message):
    if await CheckFollow.check_follow(message.bot, message.from_user.id):
        await message.answer(InviteMessage.message)


# Handler to keyboard "Контактная информация"
async def kb_contact_info(message: types.Message):
    if await CheckFollow.check_follow(message.bot, message.from_user.id):
        await message.answer(ContactInformationMessage.message)


def register_other_handlers(dp: Dispatcher):
    dp.register_message_handler(cmd_start, commands = "start")
    dp.register_message_handler(cmd_help, commands = "help")
    dp.register_message_handler(kb_mainMenuWithoutState, Text(equals = "Главное меню"))
    dp.register_message_handler(kb_mainMenuWithState, Text(equals = "Главное меню"), state = '*')
    dp.register_message_handler(kb_rules_of_application, Text(equals = "Правила составления заявки"))
    dp.register_message_handler(kb_rules_for_executors, Text(equals = "Правила для исполнителей"))
    dp.register_message_handler(kb_order_commercial, Text(equals = "Заказать рекламу в канале"))
    dp.register_message_handler(kb_make_application, Text(equals =" Составить заявку"))
    dp.register_message_handler(kb_invite, Text(equals = "Пригласить человека в канал"))
    dp.register_message_handler(kb_contact_info, Text(equals = "Контактная информация"))
