# telegram_bot/handlers.py
from aiogram import Router, F
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from sqlalchemy.orm import Session
from database import SessionLocal
from models.user import User
from aiogram.types import WebAppInfo

router = Router()

@router.message(F.text == "/start")
async def start_handler(message: Message):
    kb = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="📱 Поделиться контактом", request_contact=True)]],
        resize_keyboard=True
    )
    await message.answer(
        "👋 Привет! Поделись своим номером телефона, чтобы войти.",
        reply_markup=kb
    )


@router.message(F.contact)
async def contact_handler(message: Message):
    contact = message.contact

    # ✅ Защита — нельзя отправлять чужой контакт
    if contact.user_id != message.from_user.id:
        await message.answer("❌ Это не ваш контакт! Нажмите 'Поделиться контактом'.")
        return

    phone = contact.phone_number.replace("+", "").strip()
    telegram_id = message.from_user.id

    db: Session = SessionLocal()
    user = db.query(User).filter(User.phone_number == phone).first()

    # ❌ Пользователь не найден
    if not user:
        await message.answer("❌ Пользователь с этим номером не найден.")
        db.close()
        return

    # ✅ Привязываем Telegram ID, если его ещё нет
    if not user.telegram_id:
        user.telegram_id = telegram_id
        db.commit()
    # ❌ Если уже есть, но другой Telegram ID — блокируем
    elif user.telegram_id != telegram_id:
        await message.answer("⚠️ Этот номер уже привязан к другому Telegram-аккаунту.")
        db.close()
        return

    # ✅ Формируем ссылку на WebApp с telegram_id
    link = f"https://kpp-system.vercel.app?telegram_id={telegram_id}"

    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🔐 Открыть КПП WebApp",
                    web_app=WebAppInfo(url=link)
                )
            ]
        ]
    )

    await message.answer(
        f"✅ Добро пожаловать, {user.full_name}!\n"
        f"Ваша роль: <b>{user.role}</b>\n"
        f"Склад ID: {user.warehouse_id}\n\n"
        "Нажмите кнопку ниже, чтобы открыть WebApp:",
        reply_markup=kb,
        parse_mode="HTML"
    )

    db.close()