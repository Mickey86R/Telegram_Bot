from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

from aiogram.utils.markdown import text

from emoji import emojize

#text_paying = emojize(text('\N{credit card} Оплатить'))
text_paying = emojize(text(':warning: Опубликовать'))

buttons = [
        InlineKeyboardButton(text = text_paying, callback_data = 'Paying'),
    ]

to_pay_keyboard = InlineKeyboardMarkup()
to_pay_keyboard.add(*buttons)

