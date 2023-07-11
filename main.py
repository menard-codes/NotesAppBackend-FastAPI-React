from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm.exc import UnmappedInstanceError

from schemas import NoteInput

from model.database import DBSession
from model import models

app = FastAPI()

origins = [
    "http://localhost:5173",
    "https://notes-app-frontend-fast-api-react.vercel.app"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.get("/notes")
def read_notes():
    db = DBSession()

    try:
        notes = db.query(models.Note).all()
    finally:
        db.close()

    return notes


@app.post("/note")
def add_note(note: NoteInput):
    db = DBSession()

    try:
        if len(note.title) == 0 and len(note.note_body) == 0:
            raise HTTPException(
                status_code=400, detail={
                    "status": "Error 400 - Bad Request",
                    "msg": "Both 'title' and 'note_body' are empty. These are optional attributes but at least one must be provided."
                })

        new_note = models.Note(
            title=note.title, note_body=note.note_body
        )

        db.add(new_note)
        db.commit()
        db.refresh(new_note)
    finally:
        db.close()

    return new_note


@app.put("/note/{note_id}")
def update_note(note_id: int, updated_note: NoteInput):
    if len(updated_note.title) == 0 and len(updated_note.note_body) == 0:
        raise HTTPException(status_code=400, detail={
            "status": "Error 400 - Bad Request",
            "msg": "The note's `title` and `note_body` can't be both empty"
        })

    db = DBSession()

    try:
        note = db.query(models.Note).filter(models.Note.id == note_id).first()

        note.title = updated_note.title
        note.note_body = updated_note.note_body

        db.commit()
        db.refresh(note)
    finally:
        db.close()

    return note


@app.delete("/note/{note_id}")
def delete_note(note_id: int):
    db = DBSession()

    try:
        note = db.query(models.Note).filter(models.Note.id == note_id).first()

        db.delete(note)
        db.commit()
    except UnmappedInstanceError:
        raise HTTPException(status_code=400, detail={
            "status": "Error 400 - Bad Request",
            "msg": f"Note with `id`: `{note_id}` doesn't exist."
        })
    finally:
        db.close()

    return {
        "status": "200",
        "msg": "Note deleted successfully"
    }
