from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.database.connection import Base, engine

from app.models.user import User
from app.models.subject import Subject
from app.models.note import Note

from app.routes import auth, subjects, notes


@asynccontextmanager
async def lifespan(app: FastAPI):

    # Runs when FastAPI starts
    Base.metadata.create_all(bind=engine)

    yield

    # Runs when FastAPI shuts down
    # (nothing needed right now)


app = FastAPI(
    lifespan=lifespan
)

app.include_router(auth.router)
app.include_router(subjects.router)
app.include_router(notes.router)


@app.get("/")
def root():
    return {
        "message": "StudyHub API running"
    }