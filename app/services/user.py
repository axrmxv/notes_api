from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.models import User
from app.core.security import get_password_hash
from app.schemas.user import UserCreate
from app.core.logger import get_logger
from app.core.config import LOG_FILE


logger = get_logger("app.service.user", log_file=LOG_FILE)


class UserService:
    def __init__(self, db: AsyncSession):
        self.db = db

    # Получение всех пользователей
    async def get_all_users(self):
        result = await self.db.execute(select(User))
        users = result.scalars().all()
        logger.info(f"Retrieved {len(users)} users")
        return users

    # Создание нового пользователя
    async def create_user(self, user_data: UserCreate):
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
            f"Created user '{user_data.username}' with role '{user_data.role}'"
        )
        return new_user
