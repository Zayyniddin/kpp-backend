from datetime import datetime, timedelta
from sqlalchemy import Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from models.base import Base
import secrets

class AuthCode(Base):
    __tablename__ = "auth_codes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    code: Mapped[str] = mapped_column(String(16), unique=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    expires_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)

    @staticmethod
    def generate(user_id: int):
        """Создаёт одноразовый код"""
        return AuthCode(
            code=secrets.token_hex(4),  # пример: 'a1b2c3d4'
            user_id=user_id,
            expires_at=datetime.utcnow() + timedelta(minutes=1)
        )