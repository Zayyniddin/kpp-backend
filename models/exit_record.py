from datetime import datetime
from sqlalchemy import Integer, String, DateTime, ForeignKey, func, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from models.base import Base

class ExitRecord(Base):
    __tablename__ = "exit_records"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    pass_number: Mapped[str] = mapped_column(String(50), unique=True)
    places_count: Mapped[int | None] = mapped_column(Integer)          # NEW
    direction: Mapped[str | None] = mapped_column(String(120))         # NEW
    project: Mapped[str | None] = mapped_column(String(100))           # NEW
    comment: Mapped[str | None] = mapped_column(String(255))

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    exit_time: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    is_active: Mapped[bool] = mapped_column(Boolean, default=False)

    warehouse_id: Mapped[int] = mapped_column(ForeignKey("warehouses.id", ondelete="CASCADE"))
    warehouse = relationship("Warehouse")