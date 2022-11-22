from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

mainMenu_button = KeyboardButton('Главное меню')

mainMenu_Keyboard = ReplyKeyboardMarkup(resize_keyboard = True)
mainMenu_Keyboard.add(mainMenu_button)