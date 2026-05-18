from fastapi import FastAPI
from app.routes import auth

from app.database.connection import engine, Base

from app.models.user import User
Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth.router)

@app.get("/")
def root():
    return {"message": "StudyHub API running"}