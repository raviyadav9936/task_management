from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from modules.auth.oauth import create_access_token, get_current_user
from modules.auth.schema import UserCreate
from modules.auth.crud import create_user, authenticate_user
from database.database import get_db

router = APIRouter()

@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    new_user = create_user(db, user.username, user.password)
    return {"message": "User created", "id": new_user.id}


@router.post("/login")
def login(user: UserCreate, db: Session = Depends(get_db)):
    auth_user = authenticate_user(db, user.username, user.password)
    if not auth_user:
        raise HTTPException(status_code=400, detail="Invalid Credentials")

    token = create_access_token({"user_id": auth_user.id})
    return {"access_token": token, "token_type": "bearer"}


@router.get("/profile")
def profile(current_user=Depends(get_current_user)):
    return {"username": current_user.username, "id": current_user.id}




























