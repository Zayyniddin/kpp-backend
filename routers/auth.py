from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from models.user import User
from models.auth_code import AuthCode
from core.security import create_access_token
from database import get_db

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/generate-code")
def generate_code(telegram_id: int, db: Session = Depends(get_db)):
    """1️⃣ Вызывается ботом: проверяет telegram_id и phone_number"""
    user = db.query(User).filter(User.telegram_id == telegram_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")

    # создаём одноразовый код
    auth_code = AuthCode.generate(user.id)
    db.add(auth_code)
    db.commit()
    return {"status": "ok", "code": auth_code.code}


@router.get("/login-by-code")
def login_by_code(code: str, db: Session = Depends(get_db)):
    """2️⃣ Вызывается фронтом из WebApp"""
    record = db.query(AuthCode).filter(AuthCode.code == code).first()

    if not record or record.expires_at < datetime.utcnow():
        raise HTTPException(status_code=401, detail="Код недействителен")

    user = db.query(User).filter(User.id == record.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")

    # удаляем код (одноразовый)
    db.delete(record)
    db.commit()

    token = create_access_token(user)
    return {
        "access_token": token,
        "user": {
            "id": user.id,
            "full_name": user.full_name,
            "role": user.role,
            "warehouse_id": user.warehouse_id
        }
    }
