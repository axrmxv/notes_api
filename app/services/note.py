from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException, status

from app.db.models import Note, User
from app.schemas.note import NoteCreate, NoteUpdate
from app.core.logger import get_logger
from app.core.config import LOG_FILE

from typing import Sequence, Dict


logger = get_logger("app.service.note", log_file=LOG_FILE)


class NoteService:
    """
    Сервис для работы с заметками пользователя.

    Этот сервис включает в себя методы для создания, получения, обновления,
    удаления и восстановления заметок, а также административные функции.
    """
    def __init__(self, db: AsyncSession):
        """
        Инициализация сервиса заметок.

        Аргументы:
            db (AsyncSession): Асинхронная сессия для взаимодействия с БД.
        """
        self.db = db

    async def create_note(
        self, note_data: NoteCreate, user: User
    ) -> Note:
        """
        Создание новой заметки.

        Аргументы:
            note_data (NoteCreate): Данные для создания заметки.
            user (User): Текущий авторизованный пользователь.

        Возвращает:
            NoteResponse: Созданная заметка в виде Pydantic модели.
        """
        note = Note(
            title=note_data.title, body=note_data.body, user_id=user.id
        )
        self.db.add(note)
        try:
            await self.db.commit()
            await self.db.refresh(note)
            logger.info(f"Note created with id: {note.id} for user: {user.id}")
        except Exception as e:
            await self.db.rollback()
            logger.error("Error creating note", exc_info=e)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error"
            )
        logger.info(f"User '{user.username}' created note ID {note.id}")
        return note

    async def get_user_notes(self, user: User) -> Sequence[Note]:
        """
        Получение всех заметок текущего пользователя.

        Аргументы:
            user (User): Текущий авторизованный пользователь.

        Возвращает:
            List[NoteResponse]: Список заметок пользователя в
            виде Pydantic моделей.
        """
        result = await self.db.execute(
            select(Note).where(
                Note.user_id == user.id, Note.is_deleted.is_(False)
            )
        )
        notes = result.scalars().all()
        logger.info(f"User '{user.username}' retrieved {len(notes)} notes")
        return notes

    async def get_note_by_id(self, note_id: int, user: User) -> Note:
        """
        Получение заметки по ее ID.

        Аргументы:
            note_id (int): ID заметки.
            user (User): Текущий авторизованный пользователь.

        Возвращает:
            NoteResponse: Найденная заметка в виде Pydantic модели.

        Исключения:
            HTTPException: Если заметка не найдена.
        """
        result = await self.db.execute(
            select(Note).where(
                Note.id == note_id,
                Note.user_id == user.id,
                Note.is_deleted.is_(False)
            )
        )
        note = result.scalars().first()
        if not note:
            logger.warning(f"Note {note_id} not found for user {user.id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Note not found"
            )
        logger.info(f"User '{user.username}' retrieved {note.id} note")
        return note

    async def update_note(
        self, note_id: int, note_data: NoteUpdate, user: User
    ) -> Note:
        """
        Обновление заметки.

        Аргументы:
            note_id (int): ID заметки для обновления.
            note_data (NoteUpdate): Данные для обновления.
            user (User): Текущий авторизованный пользователь.

        Возвращает:
            NoteResponse: Обновленная заметка в виде Pydantic модели.

        Исключения:
            HTTPException: Если заметка не найдена.
        """
        result = await self.db.execute(
            select(Note).where(Note.id == note_id, Note.user_id == user.id)
        )
        note = result.scalars().first()
        if not note:
            logger.warning(
                f"Note {note_id} not found for update by user {user.id}"
            )
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Note not found"
            )

        note.title = note_data.title or note.title
        note.body = note_data.body or note.body

        try:
            await self.db.commit()
            await self.db.refresh(note)
            logger.info(f"Note {note_id} updated for user {user.id}")
        except Exception as e:
            await self.db.rollback()
            logger.error(f"Error updating note {note_id}", exc_info=e)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error"
            )
        return note

    async def delete_note(self, note_id: int, user: User) -> Dict:
        """
        Удаление (мягкое) заметки по ID.

        Аргументы:
            note_id (int): ID заметки для удаления.
            user (User): Текущий авторизованный пользователь.

        Возвращает:
            HTTPException: Если заметка не найдена.
        """
        result = await self.db.execute(
            select(Note).where(Note.id == note_id, Note.user_id == user.id)
        )
        note = result.scalars().first()
        if not note:
            logger.warning(
                f"Note {note_id} not found for deletion by user {user.id}"
            )
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Note not found"
            )
        note.is_deleted = True
        try:
            await self.db.commit()
            logger.info(f"Note {note_id} marked as deleted for user {user.id}")
        except Exception as e:
            await self.db.rollback()
            logger.error(f"Error deleting note {note_id}", exc_info=e)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error"
            )
        return {"message": f"Заметка ID {note.id} удалена"}

    # Методы для административных действий можно добавить аналогичным образом:
    async def get_all_notes(self) -> Sequence[Note]:
        """
        Получение всех заметок (для администратора).

        Возвращает:
            List[NoteResponse]: Список всех заметок в виде
            Pydantic моделей.
        """
        result = await self.db.execute(select(Note))
        notes = result.scalars().all()
        return notes

    async def get_user_notes_admin(
        self, user_id: int
    ) -> Sequence[Note]:
        """
        Получение заметок пользователя (для администратора).

        Аргументы:
            user_id (int): ID пользователя, чьи заметки нужно получить.

        Возвращает:
            List[NoteResponse]: Список заметок указанного пользователя в
            виде Pydantic моделей.
        """
        result = await self.db.execute(
            select(Note).where(Note.user_id == user_id)
        )
        notes = result.scalars().all()
        return notes

    async def restore_note(self, note_id: int) -> Dict:
        """
        Восстановление удаленной заметки.

        Аргументы:
            note_id (int): ID заметки для восстановления.

        Возвращает:
            HTTPException: Если заметка не найдена.
        """
        result = await self.db.execute(
            select(Note).where(Note.id == note_id, Note.is_deleted.is_(True))
        )
        note = result.scalars().first()
        if not note:
            logger.warning(f"Note {note_id} not found for restore")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Note not found"
            )
        note.is_deleted = False
        try:
            await self.db.commit()
            logger.info(f"Note {note_id} restored")
        except Exception as e:
            await self.db.rollback()
            logger.error(f"Error restoring note {note_id}", exc_info=e)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error"
            )
        return {"message": f"Заметка ID {note.id} востановлена"}
