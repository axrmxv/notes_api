from pydantic import BaseModel


class NoteBase(BaseModel):
    title: str
    body: str


class NoteCreate(NoteBase):
    pass


class NoteUpdate(BaseModel):
    title: str | None
    body: str | None


class NoteResponse(NoteBase):
    id: int
    user_id: int
    is_deleted: bool

    class ConfigDict:
        from_attributes = True
