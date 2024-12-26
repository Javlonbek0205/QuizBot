from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# level keyboards
level_kbs = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='a2', callback_data='a2'), KeyboardButton(text='b1', callback_data='b1')],
    [KeyboardButton(text='b2', callback_data='b2'), KeyboardButton(text='c1', callback_data='c1')],
    [KeyboardButton(text='Check', callback_data='check'), KeyboardButton(text='Skip', callback_data='skip')]
],
one_time_keyboard=True,
resize_keyboard=True)