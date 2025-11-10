from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from datetime import datetime
from fastapi import Query

from database import get_db
from models import entry_record, exit_record, warehouse
from schemas import entry_schema, exit_schema
from core.telegram_notifier import notify_tg
from models.user import User
from core.roles import check_role

router = APIRouter(prefix="/guard", tags=["Guard"])


@router.post("/entry", response_model=entry_schema.EntryRead)
def create_entry(
    data: entry_schema.EntryCreate,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(check_role("guard")),
    db: Session = Depends(get_db),
):
    rec = entry_record.EntryRecord(
        **data.model_dump(),
        warehouse_id=current_user.warehouse_id,
        is_active=True
    )
    db.add(rec)
    db.commit()
    db.refresh(rec)

    wh = db.get(warehouse.Warehouse, rec.warehouse_id)
    if wh:
        text = (
            f"🚛 <b>Новая машина на КПП</b>\n"
            f"🏢 Склад: {wh.name}\n"
            f"🔷 Номер: {rec.plate_number}\n"
            f"🏷 Проект: {rec.project or '—'}\n"
            f"🧍‍♂️ Водитель: {rec.driver_name}\n"
            f"📞 Телефон: +{rec.driver_phone or '—'}\n"
            f"💬 Комментарий: {rec.comment or '—'}\n"
            f"⏳ Въезд: {rec.created_at.strftime('%d/%m/%Y %H:%M')}\n"
        )
        notify_tg(background_tasks, wh.telegram_group_id, text)

    return rec


@router.post("/exit", response_model=exit_schema.ExitRead)
def mark_exit(
    pass_number: str,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(check_role("guard")),
    db: Session = Depends(get_db),
):
    rec = db.query(exit_record.ExitRecord).filter_by(pass_number=pass_number).first()
    if not rec:
        raise HTTPException(status_code=404, detail="Пропуск не найден")

    if rec.warehouse_id != current_user.warehouse_id:
        raise HTTPException(status_code=403, detail="Недоступно для этого склада")

    rec.is_active = True
    rec.exit_time = datetime.now()
    db.commit()
    db.refresh(rec)

    wh = db.get(warehouse.Warehouse, rec.warehouse_id)
    if wh:
        text = (
            f"📤 <b>Машина покинула склад</b>\n"
            f"🏢 Склад: {wh.name}\n"
            f"🧾 Пропуск: {rec.pass_number}\n"
            f"📦 Мест: {rec.places_count or '—'}\n"
            f"🧭 Направление: {rec.direction or '—'}\n"
            f"🏷 Проект: {rec.project or '—'}\n"
            f"💬 Комментарий: {rec.comment or '—'}\n"
            f"⏱ Выезд: {rec.exit_time.strftime('%d/%m/%Y %H:%M')}\n"
        )
        try:
            notify_tg(background_tasks, wh.telegram_group_id, text)
        except Exception as e:
            print(f"⚠️ Telegram notify error: {e}")

    return rec