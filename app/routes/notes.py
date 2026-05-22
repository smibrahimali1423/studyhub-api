from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from fastapi import HTTPException

from app.database.session import get_db

from typing import List

from app.models.note import Note
from app.models.subject import Subject
from app.models.user import User

from app.schemas.note import (
    NoteCreate,
    NoteResponse
)

from app.auth.dependencies import get_current_user

router = APIRouter(
    prefix="/notes",
    tags=["Notes"]
)

@router.post(
    "/",
    response_model=NoteResponse
)
def create_note(
    note: NoteCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    subject = db.query(Subject).filter(
        Subject.id == note.subject_id,
        Subject.user_id == current_user.id
    ).first()

    if not subject:
        return {
            "error": "Subject not found"
        }
    new_note = Note(
        title=note.title,
        content=note.content,
        subject_id=note.subject_id
    )

    db.add(new_note)
    db.commit()
    db.refresh(new_note)

    return new_note

@router.get(
    "/",
    response_model=List[NoteResponse]
)
def get_notes(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    notes = db.query(Note).join(Subject).filter(
        Subject.user_id == current_user.id
    ).all()

    return notes

@router.get(
    "/subject/{subject_id}",
    response_model=List[NoteResponse]
)
def get_notes_by_subject(
    subject_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    
    subject = db.query(Subject).filter(
        Subject.id == subject_id,
        Subject.user_id == current_user.id
    ).first()

    if not subject:
        return {
            "error": "Subject not found"
        }
    
    notes = db.query(Note).filter(
        Note.subject_id == subject_id
    ).all()

    return notes

@router.delete("/{note_id}")
def delete_note(
    note_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    note = db.query(Note).join(Subject).filter(
        Note.id == note_id,
        Subject.user_id == current_user.id
    ).first()

    if not note:
        return {
            "error": "Note not found"
        }

    db.delete(note)

    db.commit()

    return {
        "message": "Note deleted successfully"
    }