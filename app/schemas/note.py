from pydantic import BaseModel

class NoteCreate(BaseModel):
    title: str

    content: str

    subject_id: int

class NoteResponse(BaseModel):
    id: int

    title: str

    content: str
    
    subject_id: str

    class Config:

        from_attributes = True