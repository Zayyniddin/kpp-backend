# kpp/models/user.py
from sqlalchemy import Integer, String, Boolean, ForeignKey, Enum, BigInteger
from sqlalchemy.orm import Mapped, mapped_column, relationship
from enum import Enum as PyEnum
from models.base import Base

class UserRole(str, PyEnum):
    GUARD = "guard"
    DISPATCHER = "dispatcher"
    ADMIN = "admin"

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    full_name: Mapped[str] = mapped_column(String(200), nullable=False)
    phone_number: Mapped[str] = mapped_column(String(32), unique=True, index=True)
    role: Mapped[UserRole] = mapped_column(Enum(UserRole), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    telegram_id: Mapped[int | None] = mapped_column(BigInteger, unique=True, nullable=True)

    warehouse_id: Mapped[int | None] = mapped_column(ForeignKey("warehouses.id", ondelete="SET NULL"))
    warehouse = relationship("models.warehouse.Warehouse", back_populates="users")

    def __repr__(self):
        return f"<User {self.full_name} ({self.role})>"

# 👇 добавляем этот импорт, чтобы SQLAlchemy "увидел" Warehouse
from models.warehouse import Warehouse  # noqa