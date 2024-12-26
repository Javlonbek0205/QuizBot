from aiogram import Bot, Dispatcher, types
import asyncio
from aiogram.types import BotCommand
from config import BOT_TOKEN
from routers import register_routers
from database.user_db import create_database
from database.question_db import create_questions

# Bot va Dispatcher yaratish

# Botni ishga tushirish
async def on_startup():
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()
    register_routers(dp)
    await create_database()
    await create_questions()# Bazani yaratish
    print("Bot ishga tushdi!")
    await bot.set_my_commands([
        BotCommand(command="/start", description="Start the bot"),
        BotCommand(command="/help", description="Get help"),
        BotCommand(command="/myinfo", description="Get my info")
    ])
    await dp.start_polling(bot)




if __name__ == "__main__":
    asyncio.run(on_startup())
