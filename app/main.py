from fastapi import FastAPI
from app.routes import auth, subjects, notes
from app.models.subject import Subject
from app.models.note import Note

from app.database.connection import engine, Base

from app.models.user import User
Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth.router)
app.include_router(subjects.router)
app.include_router(notes.router)

@app.get("/")
def root():
    return {"message": "StudyHub API running"}

