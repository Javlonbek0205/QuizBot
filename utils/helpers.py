from aiogram import Bot
from aiogram.types import Message
from database.user_db import UserDatabase
#from helpers import user_ids
db = UserDatabase()

async def help_command(message: Message, bot: Bot):
    help_me = """
    <b>Bot commands</b>
    ✨ /start - Start the bot
    🆘 /help - Show this help message
    👤 /myinfo - Show my info
    ✍️ This is Quiz Bot
    """
    await bot.send_message(message.from_user.id, help_me,  parse_mode="HTML")

async def handle_user_info(chat_id, bot):
    try:
        chat = await bot.get_chat(chat_id)
        return {
            "id": chat.id,
            "first_name": chat.first_name,
            "last_name": chat.last_name,
            "username": chat.username,
        }
    except Exception as e:
        print(f"Error: {e}")
        return None

# async def get_info(message: Message, bot: Bot):
#     user_id = message.from_user.id  # Foydalanuvchi ID sini olish
#     user_info = await handle_user_info(user_ids[0], bot)
#
#     if user_info:
#         await message.answer(
#             f"Profil ma'lumotlari:\n"
#             f"ID: {user_info['id']}\n"
#             f"Ism: {user_info['first_name']}\n"
#             f"Familiya: {user_info['last_name'] or 'Yo\'q'}\n"
#             f"Username: @{user_info['username'] or 'Yo\'q'}"
#         )
#     else:
#         await message.answer(
#             "Profil ma'lumotlarini olishda xatolik yuz berdi! "
#             "Iltimos, bot bilan aloqa qilinganligiga ishonch hosil qiling."
#         )


async def get_info(message: Message, bot: Bot):
    user_id = message.from_user.id  # Foydalanuvchi ID sini olish
    chat_ids = await db.get_user()  # Barcha foydalanuvchi chat_id larini olish
    user = await db.get_info(user_id)  # Foydalanuvchi ma'lumotlarini olish

    if user_id in chat_ids:  # Foydalanuvchi mavjudligini tekshirish
        if user:  # Foydalanuvchi ma'lumotlari muvaffaqiyatli olingan bo'lsa
            name, user_level, points = user
            my_info = (f"📋 Your info:\n\n"
                       f"👤 Name: {name}\n"
                       f"📈 Your level: {user_level}\n"
                       f"🪙 Your points: {points}")
            await bot.send_message(message.from_user.id, my_info, parse_mode="HTML")
        else:
            await bot.send_message(message.from_user.id, "Ma'lumotlarni olishda xatolik yuz berdi.")
    else:  # Foydalanuvchi bazada yo'q bo'lsa
        await bot.send_message(
            message.from_user.id,
            "Sizning ma'lumotlaringiz bazada mavjud emas. Iltimos, oldin ro'yxatdan o'ting!"
        )

async def change_my_info(message: Message, bot: Bot):
    pass