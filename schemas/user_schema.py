from pydantic import BaseModel
from models.user import UserRole

class UserBase(BaseModel):
    full_name: str
    phone_number: str
    role: UserRole

class UserCreate(UserBase):
    warehouse_id: int | None = None

class UserRead(UserBase):
    id: int
    is_active: bool
    warehouse_id: int | None

    class Config:
        from_attributes = True