from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import sessionLocal
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse
from app.auth.security import hashed_pass

from app.schemas.user import UserCreate, UserResponse, UserLogin, Token
from app.auth.security import hashed_pass, verify_pass
from app.auth.jwt import create_access_token

from app.auth.dependencies import get_current_user

router = APIRouter(prefix="/auth", tags=["auth"])

def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/register", response_model=UserResponse)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = User(
        email=user_data.email,
        hashed_pass=hashed_pass(user_data.password),
        full_name=user_data.full_name,
        role=user_data.role,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.post("/login", response_model=Token)
def login(credentials: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == credentials.email).first()

    if not user or not verify_pass(credentials.password, user.hashed_pass):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    access_token = create_access_token(data={"sub": str(user.id), "role": user.role.value})
    return Token(access_token=access_token)

@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user