from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

from aiogram.utils.markdown import text

from emoji import emojize

text_ok = emojize(text('\u2705\nOk'))
text_decline = emojize(text('\N{cross mark}\nNo'))

buttons = [
        InlineKeyboardButton(text = text_ok, callback_data = 'Payment_ok'),
        InlineKeyboardButton(text = text_decline, callback_data = 'Payment_no'),
    ]

setChoise_keyboard = InlineKeyboardMarkup()
setChoise_keyboard.add(*buttons)
