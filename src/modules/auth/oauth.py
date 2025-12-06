from passlib.context import CryptContext
from fastapi import HTTPException, Request, Depends
from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from database.database import get_db
from database.models import User


# Secret & Algo
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Password Hash Context
pwd_cxt = CryptContext(
    schemes=["argon2"], 
    deprecated="auto"
)

class Hash:
    @staticmethod
    def bcrypt(password: str):
        return pwd_cxt.hash(password)

    @staticmethod
    def verify(plain_password: str, hashed_password: str):
        return pwd_cxt.verify(plain_password, hashed_password)


def create_access_token(data: dict):
    # JWT token create
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def verify_token(token: str):
    # Token decode and verify
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload  # dict return({"user_id": 1})
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")


class JWTBearer(HTTPBearer):
    """Custom Auth Dependency"""
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credentials and credentials.scheme.lower() == "bearer":
            return verify_token(credentials.credentials)
        raise HTTPException(status_code=403, detail="Invalid authorization header.")


def get_current_user(payload: dict = Depends(JWTBearer()), db: Session = Depends(get_db)):
    # Payload user validate
    user_id: int = payload.get("user_id")
    if not user_id:
        raise HTTPException(status_code=401, detail="User not found in token")

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    return user
