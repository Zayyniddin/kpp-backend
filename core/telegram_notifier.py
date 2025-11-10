# kpp/core/telegram_notifier.py
from aiogram import Bot
from fastapi import BackgroundTasks
from core.config import settings

bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)


async def send_message(chat_id: int, text: str):
    """Асинхронно отправляет сообщение в Telegram."""
    try:
        await bot.send_message(chat_id=chat_id, text=text, parse_mode="HTML")
    except Exception as e:
        print(f"❌ Telegram send error: {e}")


def notify_tg(background_tasks: BackgroundTasks, chat_id: int, text: str):
    """
    Универсальный вызов из синхронных эндпоинтов FastAPI.
    Добавляет задачу на отправку сообщения в фоновом режиме.
    """
    background_tasks.add_task(send_message, chat_id, text)