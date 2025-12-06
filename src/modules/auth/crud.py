from .oauth import Hash
from fastapi import HTTPException
from sqlalchemy.orm import Session
from database.models import User


def create_user(db: Session, username: str, password: str):
    try:
        user = db.query(User).filter(User.username == username).first()

        if user:
            raise HTTPException(status_code=400, detail="Username already exists")

        hashed_pw = Hash.bcrypt(password)  

        new_user = User(username=username, password=hashed_pw)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    
    except Exception as e:
        print('error',e)
        return {'status':False,'message':'Something went wrogn'}


def authenticate_user(db: Session, username: str, password: str):
    try:
        user = db.query(User).filter(User.username == username).first()
        if not user:
            return False
        if not Hash.verify(password, user.password):  
            return False
        return user
    except Exception as e:
        print('error',e)
        return {'status':False,'message':'Something went wrogn'}

