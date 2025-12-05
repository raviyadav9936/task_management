from sqlalchemy.orm import Session
from database.models import User, Task
from fastapi import HTTPException

# User CRUD
def create_user(db: Session, username: str, password: str):
    user = db.query(User).filter(User.username == username).first()

    if user:
        raise HTTPException(status_code=400, detail="Username already exists")
    
    new_user = User(username=username, password=password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def authenticate_user(db: Session, username: str, password: str):
    user = db.query(User).filter(User.username == username, User.password == password).first()
    return user