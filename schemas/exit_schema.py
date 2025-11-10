from pydantic import BaseModel
from datetime import datetime

class ExitBase(BaseModel):
    pass_number: str
    places_count: int | None = None
    direction: str | None = None
    project: str | None = None
    comment: str | None = None

class ExitCreate(ExitBase):
    pass

class ExitRead(ExitBase):
    id: int
    created_at: datetime
    exit_time: datetime | None
    is_active: bool

    class Config:
        from_attributes = True