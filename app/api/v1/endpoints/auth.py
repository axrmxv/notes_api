from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.db.session import get_db
from app.db.models import User
from app.schemas.auth import Token
from app.schemas.user import UserResponse, UserCreate
from app.core.security import create_access_token
from app.core.config import ACCESS_TOKEN_EXPIRE_MINUTES
from app.core.security import get_password_hash, verify_password
from typing import Annotated


router = APIRouter()


@router.post("/token")
async def login_for_access_token(
    user_in: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: AsyncSession = Depends(get_db)
) -> Token:
    """
    Авторизация пользователя для получения токена доступа.

    Принимает данные пользователя в формате OAuth2PasswordRequestForm и
    возвращает токен доступа (JWT). Если имя пользователя или пароль неверны,
    генерируется ошибка 401 Unauthorized.

    Аргументы:
    - user_in (OAuth2PasswordRequestForm): Данные пользователя для авторизации.
    - db (AsyncSession): Сессия базы данных.

    Возвращает:
    - Token: Токен доступа в формате JWT.

    Исключения:
    - HTTPException: Ошибка 401, если имя пользователя или пароль неверны.
    """
    result = await db.execute(
        select(User).filter(User.username == user_in.username)
    )
    user = result.scalars().first()

    if not user or not verify_password(user_in.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверное имя пользователя или пароль"
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


@router.post("/register", response_model=UserResponse)
async def register(
    user_in: UserCreate, db: AsyncSession = Depends(get_db)
) -> UserResponse:
    """
    Регистрация нового пользователя.

    Создает нового пользователя в базе данных. Если пользователь с таким
    именем уже существует или если пытается зарегистрироваться администратор,
    генерируются соответствующие ошибки.

    Аргументы:
    - user_in (UserCreate): Данные для регистрации нового пользователя.
    - db (AsyncSession): Сессия базы данных.

    Возвращает:
    - UserResponse: Ответ с данными нового пользователя.

    Исключения:
    - HTTPException: Ошибка 400, если пользователь с таким
    именем уже существует.
    - HTTPException: Ошибка 403, если пытаются создать
    администратора через регистрацию.
    """
    if user_in.role == "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Нельзя создать администратора через регистрацию"
        )
    result = await db.execute(
        select(User).filter(User.username == user_in.username)
    )
    existing_user = result.scalars().first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Пользователь с таким именем уже существует"
        )

    hashed_password = get_password_hash(user_in.password)

    new_user = User(
        username=user_in.username,
        password=hashed_password,
        role=user_in.role
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    return UserResponse(
        id=new_user.id,
        username=new_user.username,
        role=new_user.role
    )
