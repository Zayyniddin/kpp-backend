# telegram_bot/bot.py
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import asyncio
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from core.config import settings
from telegram_bot.handlers import router


async def main():
    # 👇 новое: передаём parse_mode через DefaultBotProperties
    bot = Bot(
        token=settings.TELEGRAM_BOT_TOKEN,
        default=DefaultBotProperties(parse_mode="HTML")
    )

    dp = Dispatcher()
    dp.include_router(router)

    print("🚀 Bot is running...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())