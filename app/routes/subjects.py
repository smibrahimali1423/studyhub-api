from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models.subject import Subject
from app.schemas.subject import SubjectCreate, SubjectResponse
from app.auth.dependencies import get_current_user
from app.models.user import User
from typing import List

from fastapi import HTTPException

router = APIRouter(
    prefix="/subjects",
    tags=["Subjects"]
)

@router.post(
    "/",
    response_model=SubjectResponse
)
def create_subject(
    subject: SubjectCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    new_subject = Subject(
        name=subject.name,
        user_id=current_user.id
    )
 
    db.add(new_subject)

    db.commit()

    db.refresh(new_subject)

    return new_subject

@router.get(
    "/",
    response_model=List[SubjectResponse]
)
def get_subjects(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    subjects = db.query(Subject).filter(
        Subject.user_id == current_user.id
    ).all()

    return subjects

@router.get(
    "/{subject_id}",
    response_model=SubjectResponse
)
def get_subject(
    subject_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    subject = db.query(Subject).filter(
        Subject.id == subject_id,
        Subject.user_id == current_user.id
    ).first()

    if not subject:
        raise HTTPException(
            status_code=404,
            detail="Subject not found"
        )

    return subject

@router.delete("/{subject_id}")
def delete_subject(
    subject_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    subject = db.query(Subject).filter(
        Subject.id == subject_id,
        Subject.user_id == current_user.id
    ).first()

    if not subject:
        return {
            "error": "Subject not found"
        }

    db.delete(subject)

    db.commit()

    return {
        "message": "Subject deleted successfully"
    }