from app.crud.base import BaseCRUD
from app.db.models import User
from app.schemas.user import UserCreate, UserResponse
from app.core.security import get_password_hash
from sqlalchemy.ext.asyncio import AsyncSession


class UserCRUD(BaseCRUD[User, UserCreate, UserResponse]):
    def __init__(self):
        super().__init__(User)

    async def create(self, db: AsyncSession, obj_in: UserCreate, **kwargs):
        hashed_password = get_password_hash(obj_in.password)
        obj_in_data = obj_in.model_dump()
        obj_in_data["password"] = hashed_password
        # obj_in_data["hashed_password"] = hashed_password
        # obj_in_data.pop("password", None)  # Удаляем пароль перед сохранением
        return await super().create(db, obj_in, **kwargs)


user_crud = UserCRUD()
