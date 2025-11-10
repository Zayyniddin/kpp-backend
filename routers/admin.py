from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import models
from database import get_db
from schemas import project_schema, warehouse_schema, user_schema
from core.roles import check_role
from models.user import User

router = APIRouter(prefix="/admin", tags=["Admin"])

# ----------- PROJECTS -----------
@router.post("/projects", response_model=project_schema.ProjectRead)
def create_project(
    data: project_schema.ProjectCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(check_role("admin")),
):
    project = models.project.Project(**data.model_dump())
    db.add(project)
    db.commit()
    db.refresh(project)
    return project


@router.get("/projects", response_model=list[project_schema.ProjectRead])
def get_projects(
    db: Session = Depends(get_db),
    current_user: User = Depends(check_role("admin")),
):
    return db.query(models.project.Project).all()


# ----------- WAREHOUSES -----------
@router.post("/warehouses", response_model=warehouse_schema.WarehouseRead)
def create_warehouse(
    data: warehouse_schema.WarehouseCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(check_role("admin")),
):
    warehouse = models.warehouse.Warehouse(**data.model_dump())
    db.add(warehouse)
    db.commit()
    db.refresh(warehouse)
    return warehouse


@router.get("/warehouses", response_model=list[warehouse_schema.WarehouseRead])
def get_warehouses(
    db: Session = Depends(get_db),
    current_user: User = Depends(check_role("admin")),
):
    return db.query(models.warehouse.Warehouse).all()


# ----------- USERS -----------
@router.post("/users", response_model=user_schema.UserRead)
def create_user(
    data: user_schema.UserCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(check_role("admin")),
):
    user = models.user.User(**data.model_dump())
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.get("/users", response_model=list[user_schema.UserRead])
def get_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(check_role("admin")),
):
    return db.query(models.user.User).all()


@router.delete("/warehouses/{warehouse_id}")
def delete_warehouse(warehouse_id: int, db: Session = Depends(get_db)):
    warehouse = db.query(models.warehouse.Warehouse).filter_by(id=warehouse_id).first()
    if not warehouse:
        raise HTTPException(status_code=404, detail="Склад не найден")
    db.delete(warehouse)
    db.commit()
    return {"status": "ok", "message": f"Склад {warehouse.name} удалён"}


@router.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.user.User).filter_by(id=user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    db.delete(user)
    db.commit()
    return {"status": "ok", "message": f"Пользователь {user.full_name} удалён"}