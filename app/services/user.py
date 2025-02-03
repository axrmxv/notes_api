from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.models import User
from app.core.security import get_password_hash
from app.schemas.user import UserCreate
from app.core.logger import get_logger
from app.core.config import LOG_FILE

from typing import Sequence


logger = get_logger("app.service.user", log_file=LOG_FILE)


class UserService:
    """
    Сервис для администраторов.

    Позволяет получить всех пользователей и создать нового пользователя.
    """
    def __init__(self, db: AsyncSession):
        """
        Инициализация сервиса пользователей.

        Аргументы:
            db (AsyncSession): Асинхронная сессия базы данных.
        """
        self.db = db

    # Получение всех пользователей
    async def get_all_users(self) -> Sequence[User]:
        """
        Получение списка всех пользователей.

        Возвращает:
            List[User]: Список всех пользователей.
        """
        result = await self.db.execute(select(User))
        users = result.scalars().all()
        logger.info(f"Получено {len(users)} пользователей.")
        return users

    # Создание нового пользователя
    async def create_user(self, user_data: UserCreate) -> User:
        """
        Создание нового пользователя.

        Аргументы:
            user_data (UserCreate): Данные для создания нового пользователя.

        Возвращает:
            User: Созданный пользователь.
        """
        hashed_password = get_password_hash(user_data.password)
        new_user = User(
            username=user_data.username,
            password=hashed_password,
            role=user_data.role
        )
        self.db.add(new_user)
        await self.db.commit()
        await self.db.refresh(new_user)
        logger.info(
            f"Создан пользователь '{user_data.username}' с ролью '{user_data.role}'"
        )
        return new_user
