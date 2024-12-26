from aiogram import types
from aiogram import Dispatcher
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from states.reply_keyboards import level_kbs
from utils.helpers import help_command, get_info
from tests.test_database import user_ids, user_del
from routers import level_test
from routers.stats import SaveUser
from database.user_db import UserDatabase

db = UserDatabase()


async def start_command(message: types.Message, state: FSMContext):
    user_id = message.from_user.id  # Foydalanuvchi ID ni olish
    chat_ids = await db.get_user()  # Barcha chat_id larni olish
    print(chat_ids)  # Debug uchun natijani ko'rish

    # Foydalanuvchi ID ni bazadagi chat_id lar bilan solishtirish
    if user_id in chat_ids:
        await level_test.exist_user(message)  # Agar foydalanuvchi mavjud bo'lsa
    else:
        await non_existing_user_start(message, state)

async def non_existing_user_start(message: Message, state: FSMContext):
    await message.answer("Bot description here.")
    await message.answer("Enter your name: ")
    await state.set_state(SaveUser.name)

async def save_user(message: Message, state: FSMContext):
    user_id = message.chat.id
    # Holat ma'lumotlariga foydalanuvchi ismini saqlash
    await state.update_data(name=message.text)

    # Saqlangan holat ma'lumotlarini olish
    data = await state.get_data()
    user_name = data.get('name')  # get('name') orqali olingan ma'lumot

    # Foydalanuvchini bazaga qo'shish (TODO: Shu joyda user ma'lumotlarini bazaga qo'shing)
    try:
        await db.add_user(user_name, user_id, None, 0)
        await message.answer(f"Thanks {user_name}, you're registered!")
    except Exception as e:
        await message.answer("An error occurred during registration.")
        print(f"Error: {e}")


    # Daraja tanlash uchun xabar yuborish
    await message.answer("Pick your level", reply_markup=level_kbs)
    await state.set_state(SaveUser.level)

    #await add_user(message.chat.id, message.from_user.full_name)

def register_start(dp: Dispatcher):
    dp.message.register(start_command, Command(commands=["start"]))
    dp.message.register(help_command, Command(commands=["help"]))
    dp.message.register(get_info, Command(commands=["myinfo"]))
    dp.message.register(save_user, SaveUser.name)

