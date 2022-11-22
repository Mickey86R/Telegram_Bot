from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton


menuKeyboard = ReplyKeyboardMarkup(resize_keyboard = True)

rulesOfMakingApplication_button = KeyboardButton('Правила составления заявки')
rulesForExecutors_button = KeyboardButton('Правила для исполнителей')

orderCommercial_button = KeyboardButton('Заказать рекламу в канале')
makeApplication_button = KeyboardButton('Составить заявку')

inviteToChannel_button = KeyboardButton('Пригласить человека в канал')
contactInformation_button = KeyboardButton('Контактная информация')

buttons1 = ['Правила составления заявки', 'Правила для исполнителей']
buttons2 = ['Заказать рекламу в канале', 'Составить заявку']
buttons3 = ['Пригласить человека в канал', 'Контактная информация']

menuKeyboard.add(*buttons1)
menuKeyboard.add(*buttons2)
menuKeyboard.add(*buttons3)