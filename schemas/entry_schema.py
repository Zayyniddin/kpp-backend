from pydantic import BaseModel
from datetime import datetime

class EntryBase(BaseModel):
    plate_number: str
    project: str | None = None
    driver_name: str
    driver_phone: str | None = None
    comment: str | None = None


class EntryCreate(EntryBase):
    pass

class EntryRead(EntryBase):
    id: int
    created_at: datetime
    is_active: bool

    class Config:
        from_attributes = True