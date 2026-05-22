from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.schemas.user import UserCreate, UserResponse, UserLogin
from app.models.user import User
from app.database.session import get_db
from app.auth.hashing import hash_password, verify_password
from app.auth.jwt_handler import create_access_token
from app.auth.dependencies import get_current_user

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)

@router.get("/me")
def get_me(
    current_user: str = Depends(get_current_user)
):
    return {
        "message": "Protected route working",
        "email": current_user
    }

@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    
    existing_user = db.query(User).filter(
        User.email == user.email
    ).first()

    if not existing_user:
        return {"error": "Invalid credentials"}
    
    password_valid = verify_password(
        user.password,
        existing_user.password
    )

    access_token = create_access_token(
        data={"sub": existing_user.email}
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

@router.post("/signup", response_model=UserResponse)
def signup(user: UserCreate, db: Session = Depends(get_db)):

    hashed_password = hash_password(user.password)

    new_user = User(
        email=user.email,
        password=hashed_password
    )

    db.add(new_user)

    db.commit()

    db.refresh(new_user)

    return new_user