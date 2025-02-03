from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.note import NoteCreate, NoteUpdate, NoteResponse
from app.db.session import get_db
from app.core.security import require_role, get_current_user
from app.db.models import User
from app.services.note import NoteService

from typing import List


router = APIRouter()


def get_note_service(db: AsyncSession = Depends(get_db)) -> NoteService:
    """
    Создает и возвращает экземпляр NoteService.

    Аргументы:
        db (AsyncSession): Сессия базы данных.

    Возвращает:
        NoteService: Экземпляр сервиса для работы с заметками.
    """
    return NoteService(db)


# Создание заметки
@router.post(
    "/notes/",
    response_model=NoteResponse,
    dependencies=[Depends(require_role("user"))]
)
async def create_note(
    note_data: NoteCreate,
    user: User = Depends(get_current_user),
    note_service: NoteService = Depends(get_note_service)
) -> NoteResponse:
    """
    Создание новой заметки.

    Принимает данные заметки и создает новую заметку,
    связанную с текущим пользователем.

    Аргументы:
        note_data (NoteCreate): Данные для создания заметки.
        user (User): Текущий авторизованный пользователь.
        note_service (NoteService): Сервис для работы с заметками.

    Возвращает:
        NoteResponse: Ответ с данными созданной заметки.
    """
    note = await note_service.create_note(note_data, user)
    return note


# Получение списка заметок (только своих)
@router.get("/notes/", response_model=List[NoteResponse])
async def get_user_notes(
    user: User = Depends(require_role("user")),
    note_service: NoteService = Depends(get_note_service)
) -> List[NoteResponse]:
    """
    Получение списка заметок текущего пользователя.

    Аргументы:
        user (User): Текущий авторизованный пользователь.
        note_service (NoteService): Сервис для работы с заметками.

    Возвращает:
        List[NoteResponse]: Список заметок текущего пользователя.
    """
    notes = await note_service.get_user_notes(user)
    return notes


# Получение конкретной заметки
@router.get("/notes/{note_id}", response_model=NoteResponse)
async def get_note_by_id(
    note_id: int,
    user: User = Depends(require_role("user")),
    note_service: NoteService = Depends(get_note_service)
) -> NoteResponse:
    """
    Получение конкретной заметки по ID.

    Аргументы:
        note_id (int): ID заметки.
        user (User): Текущий авторизованный пользователь.
        note_service (NoteService): Сервис для работы с заметками.

    Возвращает:
        NoteResponse: Ответ с данными конкретной заметки.
    """
    note = await note_service.get_note_by_id(note_id, user)
    return note


# Обновление заметки
@router.put("/notes/{note_id}", response_model=NoteResponse)
async def update_note(
    note_id: int,
    note_data: NoteUpdate,
    user: User = Depends(require_role("user")),
    note_service: NoteService = Depends(get_note_service)
) -> NoteResponse:
    """
    Обновление существующей заметки.

    Аргументы:
        note_id (int): ID заметки для обновления.
        note_data (NoteUpdate): Данные для обновления заметки.
        user (User): Текущий авторизованный пользователь.
        note_service (NoteService): Сервис для работы с заметками.

    Возвращает:
        NoteResponse: Ответ с обновленными данными заметки.
    """
    note = await note_service.update_note(note_id, note_data, user)
    return note


# Удаление заметки (мягкое удаление)
@router.delete("/notes/{note_id}", response_model=dict)
async def delete_note(
    note_id: int,
    user: User = Depends(require_role("user")),
    note_service: NoteService = Depends(get_note_service)
) -> dict:
    """
    Удаление (мягкое) заметки по ID.

    Аргументы:
        note_id (int): ID заметки для удаления.
        user (User): Текущий авторизованный пользователь.
        note_service (NoteService): Сервис для работы с заметками.

    Возвращает:
        dict: Сообщение об успешном удалении заметки.
    """
    await note_service.delete_note(note_id, user)
    return {"message": "Заметка удалена"}


# Административные эндпоинты
@router.get(
    "/admin/notes/",
    response_model=List[NoteResponse],
    dependencies=[Depends(require_role("admin"))]
)
async def get_all_notes(
    note_service: NoteService = Depends(get_note_service)
) -> List[NoteResponse]:
    """
    Получение всех заметок (для администраторов).

    Аргументы:
        note_service (NoteService): Сервис для работы с заметками.

    Возвращает:
        List[NoteResponse]: Список всех заметок.
    """
    notes = await note_service.get_all_notes()
    return notes


@router.get("/admin/users/{user_id}/notes/", response_model=List[NoteResponse])
async def get_user_notes_admin(
    user_id: int,
    _: User = Depends(require_role("admin")),
    note_service: NoteService = Depends(get_note_service)
) -> List[NoteResponse]:
    """
    Получение заметок пользователя (для администратора).

    Аргументы:
        user_id (int): ID пользователя, чьи заметки нужно получить.
        note_service (NoteService): Сервис для работы с заметками.

    Возвращает:
        List[NoteResponse]: Список заметок указанного пользователя.
    """
    notes = await note_service.get_user_notes_admin(user_id)
    return notes


@router.post("/admin/notes/{note_id}/restore", response_model=dict)
async def restore_note(
    note_id: int,
    _: User = Depends(require_role("admin")),
    note_service: NoteService = Depends(get_note_service)
) -> dict:
    """
    Восстановление удаленной заметки.

    Аргументы:
        note_id (int): ID заметки для восстановления.
        note_service (NoteService): Сервис для работы с заметками.

    Возвращает:
        dict: Сообщение о восстановлении заметки.
    """
    await note_service.restore_note(note_id)
    return {"message": "Заметка востановлена"}
