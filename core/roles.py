# kpp/core/roles.py
from fastapi import Depends, HTTPException, status
from core.security import get_current_user
from models.user import User

def check_role(*allowed_roles: str):
    """
    Возвращает Depends, который проверяет роль текущего пользователя.
    Пример:
        @router.post(..., dependencies=[Depends(check_role("guard"))])
    или:
        current_user: User = Depends(check_role("dispatcher"))
    """
    def role_dependency(current_user: User = Depends(get_current_user)):
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Недостаточно прав. Разрешено: {', '.join(allowed_roles)}",
            )
        return current_user
    return role_dependency