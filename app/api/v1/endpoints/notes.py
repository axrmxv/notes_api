from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.note import NoteCreate, NoteUpdate, NoteResponse
from app.crud.note import note_crud
from app.db.session import get_db
from app.core.security import require_role, get_current_user
from app.db.models import User


router = APIRouter()


@router.post(
    "/",
    response_model=NoteResponse,
    dependencies=[Depends(require_role("user"))]
)
async def create_note(
    note: NoteCreate,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    return await note_crud.create(db, note, user_id=user.id)


@router.get("/{note_id}", response_model=NoteResponse)
async def get_note(
    note_id: int,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    return await note_crud.get(db, note_id)


@router.put("/{note_id}", response_model=NoteResponse)
async def update_note(
    note_id: int, note_update: NoteUpdate, db: AsyncSession = Depends(get_db)
):
    note = await note_crud.get(db, note_id)
    return await note_crud.update(db, note, note_update)  # type: ignore


@router.delete("/{note_id}", response_model=NoteResponse)
async def delete_note(note_id: int, db: AsyncSession = Depends(get_db)):
    note = await note_crud.get(db, note_id)
    return await note_crud.delete(db, note)  # type: ignore
