from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta, timezone

from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(plain_password: str) -> str:
    return pwd_context.hash(plain_password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    copyData = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    copyData.update({
        "exp":expire
    })
    return jwt.encode(copyData, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)

def create_refresh_token(data: dict) -> str:
     copyData = data.copy()
     expire = datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
     copyData.update({
         "exp":expire
     })
     return jwt.encode(copyData, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    
def decode_token(token: str) -> dict:
    return jwt.decode(token ,settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])