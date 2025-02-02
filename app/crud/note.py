from app.crud.base import BaseCRUD
from app.db.models import Note
from app.schemas.note import NoteCreate, NoteUpdate


class NoteCRUD(BaseCRUD[Note, NoteCreate, NoteUpdate]):
    def __init__(self):
        super().__init__(Note)


note_crud = NoteCRUD()
