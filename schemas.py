from pydantic import BaseModel


class NoteInput(BaseModel):
    title: str = ''
    note_body: str = ''
