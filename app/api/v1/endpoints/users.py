from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models import User
from app.schemas.user import UserCreate, UserResponse
from app.services.user import UserService
from app.core.security import require_role
from app.db.session import get_db


router = APIRouter()


# Получение списка всех пользователей (только для администратора)
@router.get("/users/", response_model=list[UserResponse])
async def get_all_users(
    current_user: User = Depends(require_role("admin")),
    db: AsyncSession = Depends(get_db)
):
    user_service = UserService(db)
    users = await user_service.get_all_users()
    return users


# Создание нового пользователя (роль "user" или "admin")
@router.post(
    "/users/", response_model=UserResponse, status_code=status.HTTP_201_CREATED
)
async def create_user(
    user_data: UserCreate,
    current_user: User = Depends(require_role("admin")),
    db: AsyncSession = Depends(get_db)
):
    if user_data.role not in ["user", "admin"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Role must be 'user' or 'admin'"
        )
    user_service = UserService(db)
    new_user = await user_service.create_user(user_data)
    return new_user
