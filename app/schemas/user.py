from pydantic import BaseModel
from enum import Enum


class UserBase(BaseModel):
    username: str


class UserRole(str, Enum):
    user = "user"
    admin = "admin"


class UserAuth(UserBase):
    password: str


class UserCreate(UserBase):
    password: str
    role: UserRole = UserRole.user


class UserResponse(UserBase):
    id: int
    role: str

    class ConfigDict:
        from_attributes = True
