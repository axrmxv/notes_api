from sqlalchemy import String, ForeignKey, Text
from sqlalchemy.orm import (
    DeclarativeBase, Mapped, mapped_column, declared_attr
)
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from datetime import datetime
from typing import List


class Base(DeclarativeBase):
    @declared_attr.directive
    def __tablename__(cls) -> str:
        return cls.__name__.lower()

    id: Mapped[int] = mapped_column(
        primary_key=True, index=True, autoincrement=True
    )


# Миксин для добавления общих полей в модели
class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(
        default=func.now(), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        default=func.now(), onupdate=func.now(), server_default=func.now()
    )


class User(TimestampMixin, Base):
    username: Mapped[str] = mapped_column(
        String(20), unique=True, index=True, nullable=False
    )
    password: Mapped[str] = mapped_column(String, nullable=False)
    role: Mapped[str] = mapped_column(String(20), default="user")

    notes: Mapped[List["Note"]] = relationship(back_populates="user")


class Note(TimestampMixin, Base):
    title: Mapped[str] = mapped_column(String(256), nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    is_deleted: Mapped[bool] = mapped_column(default=False)

    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    user: Mapped["User"] = relationship("User", back_populates="notes")
