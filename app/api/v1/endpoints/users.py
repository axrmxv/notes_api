from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.user import UserCreate, UserResponse
from app.crud.user import user_crud
from app.db.session import get_db


router = APIRouter()


@router.post("/", response_model=UserResponse)
async def create_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    return await user_crud.create(db, user)


@router.get("/", response_model=list[UserResponse])
async def read_users(
    skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)
):
    return await user_crud.get_all(db, skip, limit)
