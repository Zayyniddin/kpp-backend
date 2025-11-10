# kpp/models/warehouse.py
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from models.base import Base

class Warehouse(Base):
    __tablename__ = "warehouses"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100))
    address: Mapped[str] = mapped_column(String(255))
    telegram_group_id: Mapped[int | None]

    users = relationship("models.user.User", back_populates="warehouse")
    def __repr__(self):
        return f"<Warehouse {self.name}>"