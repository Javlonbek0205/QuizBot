from aiogram import  Dispatcher
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from routers.stats import SaveUser
from states.inline_keyboards import test_kbs
from routers import general_test
from  database.user_db import UserDatabase
db = UserDatabase()


async def get_level(message: Message, state: FSMContext):
    user_level = message.text
    user_id = message.from_user.id  # TODO: Save user level to database
    try:
        await db.change_user(user_id, user_level)
        await message.answer(f"Your level: {user_level}", reply_markup=ReplyKeyboardRemove())
    except Exception as e:
        await message.answer("An error occurred during registration.")
        print(f"Error: {e}")
    await state.clear()
    await exist_user(message)


async def exist_user(message: Message):
    await message.answer('Pick a test', reply_markup=test_kbs)


async def tests(callback: CallbackQuery, state: FSMContext):
    if callback.data == 'general test':
        await general_test.create_poll(message=callback.message, state=state)

def register_level(dp: Dispatcher):
    dp.message.register(get_level, SaveUser.level)
    dp.callback_query.register(tests)