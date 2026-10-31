import asyncio
import logging
import sys
from aiogram import Bot, Dispatcher
from config import settings
from database.db import init_db
from handlers import start, core

async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
        stream=sys.stdout,
    )
    
    await init_db()
    
    bot = Bot(token=settings.BOT_TOKEN)
    dp = Dispatcher()
    
    dp.include_router(start.router)
    dp.include_router(core.router)
    
    logging.info("Starting TaskMaster Pro Bot...")
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.info("Bot stopped.")