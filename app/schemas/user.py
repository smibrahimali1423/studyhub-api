from pydantic import BaseModel

class UserBase(BaseModel):
    email: str

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    pass

class UserLogin(BaseModel):
    email: str
    password: str 