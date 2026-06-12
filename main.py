from os import getenv
import asyncio
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
from db import init_db
from handlers.routes import router

load_dotenv()
Token = getenv("bot_token")

dp = Dispatcher()
dp.include_router(router)

async def main():
    await init_db()
    bot = Bot(token=Token)
    
    print("start..")
    await dp.start_polling(bot)
    
if __name__=="__main__":
    asyncio.run(main())