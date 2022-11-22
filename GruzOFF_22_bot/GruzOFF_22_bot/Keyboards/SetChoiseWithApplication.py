from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from aiogram.utils.markdown import text

from emoji import emojize

text_ok = emojize(text('\u2705\nОк'))
text_decline = emojize(text('\N{cross mark}\nНе подходит'))
text_edit = emojize(text('\N{page facing up}\nИсправить'))

buttons = [
        InlineKeyboardButton(text = text_ok, callback_data = 'AdminChoise_Confirm'),
        InlineKeyboardButton(text = text_decline, callback_data = 'AdminChoise_Decline'),
        InlineKeyboardButton(text = text_edit, callback_data = 'AdminChoise_Edit')
    ]

setChoise_keyboard = InlineKeyboardMarkup()
setChoise_keyboard.add(*buttons)
