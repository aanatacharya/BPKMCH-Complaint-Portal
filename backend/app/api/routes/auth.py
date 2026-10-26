from fastapi import APIRouter, status, HTTPException, Depends
from sqlalchemy.orm import Session
from jose import JWTError

from app.db.session import get_db
from app.schemas.user import UserCreate, UserOut
from app.crud.user import create_user, get_user_by_username
from app.schemas.auth import LoginRequest, TokenResponse
from app.core.security import verify_password, create_access_token, create_refresh_token, decode_token
from app.schemas.auth import RefreshTokenRequest

router = APIRouter()

@router.post("/register", response_model=UserOut)
def register(user_in: UserCreate, db: Session = Depends(get_db)):
    existing_user = get_user_by_username(db, user_in.username)
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already exists.")
    
    new_user = create_user(db, user_in)
    return new_user

@router.post("/login", response_model=TokenResponse)
def login(login_in: LoginRequest, db: Session = Depends(get_db)):
    this_user = get_user_by_username(db, login_in.username)
    
    if not this_user or not verify_password(login_in.password, this_user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password.")
    
    token_payload = {
        "sub": str(this_user.id),
        "role": this_user.role.value 
    }
    
    access_token = create_access_token(token_payload)
    refresh_token = create_refresh_token(token_payload)
    
    return TokenResponse(access_token=access_token, refresh_token=refresh_token)

@router.post("/refresh-token", response_model=TokenResponse)
def refresh_token(payload: RefreshTokenRequest):
    try:
        decoded_token = decode_token(payload.refresh_token)
        token_payload = {
            "sub": decode_token.get("sub"),
            "role": decode_token.get("role")
        }
        
        new_access_token = create_access_token(token_payload)
        
        return TokenResponse(access_token=new_access_token, refresh_token=payload.refresh_token)
        
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired refresh token.")
     