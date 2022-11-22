from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton


buttons = [
        InlineKeyboardButton(text = 'Сейчас', callback_data = 'Give_Now'),
        InlineKeyboardButton(text = 'Сегодня', callback_data = 'Give_Today'),
        InlineKeyboardButton(text = 'Завтра', callback_data = 'Give_Tomorrow')
    ]

setDay_keyboard = InlineKeyboardMarkup()
setDay_keyboard.add(*buttons)