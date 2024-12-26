from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

test_kbs = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='General test', callback_data='general test'),
     InlineKeyboardButton(text='IELTS test', callback_data='ielts')]
])
