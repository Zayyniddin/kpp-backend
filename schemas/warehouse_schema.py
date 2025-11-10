# kpp/schemas/warehouse_schema.py
from pydantic import BaseModel

class WarehouseBase(BaseModel):
    name: str
    address: str | None = None
    telegram_group_id: int

class WarehouseCreate(WarehouseBase):
    pass  # больше не нужно поле project_id

class WarehouseRead(WarehouseBase):
    id: int

    class Config:
        from_attributes = True