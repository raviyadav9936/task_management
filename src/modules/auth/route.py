from fastapi import APIRouter,Depends,HTTPException
from database.database import get_db
from sqlalchemy.orm import Session
from modules.auth.crud import create_user,authenticate_user
from modules.auth.oauth import create_access_token
from modules.auth.schema import UserCreate
from fastapi.security import OAuth2PasswordRequestForm



router=APIRouter()


@router.post("/register")
def register(user: UserCreate, db:Session= Depends(get_db)):
    new_user = create_user(db, user.username, user.password)
    return {"id": new_user.id, "username": new_user.username}


@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    auth_user = authenticate_user(db, form_data.username, form_data.password)
    if not auth_user:
        raise HTTPException(400, "Invalid credentials")
    token = create_access_token({"user_id": auth_user.id})
    return {"access_token": token, "token_type": "bearer"}




# @router.post("/login")
# def login(user: UserCreate, db:Session = Depends(get_db)):
#     auth_user = authenticate_user(db, user.username, user.password)
#     if not auth_user:
#         raise HTTPException(400, "Invalid credentials")
#     token = create_access_token({"user_id": auth_user.id})
#     return {"access_token": token, "token_type": "bearer"}

























