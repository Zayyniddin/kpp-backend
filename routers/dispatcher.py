from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models.exit_record import ExitRecord
from schemas.exit_schema import ExitCreate, ExitRead
from core.security import get_current_user
from models.user import User
from core.roles import check_role

router = APIRouter(prefix="/dispatcher", tags=["Dispatcher"])

@router.post("/create-pass", response_model=ExitRead)
def create_pass(data: ExitCreate, db: Session = Depends(get_db),   current_user: User = Depends(check_role("dispatcher"))):
    rec = ExitRecord(**data.model_dump(), warehouse_id=current_user.warehouse_id, is_active=False)
    db.add(rec)
    db.commit()
    db.refresh(rec)
    return rec