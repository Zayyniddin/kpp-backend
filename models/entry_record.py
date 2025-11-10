from datetime import datetime
from sqlalchemy import Integer, String, Float, DateTime, ForeignKey, func, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from models.base import Base

class EntryRecord(Base):
    __tablename__ = "entry_records"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    plate_number: Mapped[str] = mapped_column(String(20), nullable=False)
    project: Mapped[str | None] = mapped_column(String(100))          # NEW
    driver_name: Mapped[str] = mapped_column(String(100))
    driver_phone: Mapped[str | None] = mapped_column(String(32))      # NEW
    comment: Mapped[str | None] = mapped_column(String(255))

    places_count: Mapped[int | None] = mapped_column(Integer)         # legacy, не используем
    cargo_weight_kg: Mapped[float | None] = mapped_column(Float)      # legacy, не используем

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    warehouse_id: Mapped[int] = mapped_column(ForeignKey("warehouses.id", ondelete="CASCADE"))
    warehouse = relationship("Warehouse")