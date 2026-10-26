from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from jose import JWTError

from app.db.session import get_db
from app.core.security import decode_token
from app.crud.user import get_user_by_id
from app.models.user import User
from app.enums import Role

bearer_scheme = HTTPBearer()

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme), db: Session = Depends(get_db)) -> User:
    try:
        payload = decode_token(credentials.credentials)
        user_id = payload.get("sub")

        this_user = get_user_by_id(db, int(user_id))

        if this_user:
            return this_user
        else:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials.")
    except JWTError as err:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Could not validate credentials: {err}")

def require_admin(current_user: User = Depends(get_current_user)) -> User:
    if current_user.role not in (Role.admin, Role.superadmin):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin access required.")

    return current_user

def require_superadmin(current_user: User = Depends(get_current_user)) -> User:
    if current_user.role != Role.superadmin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Superadmin access required.")

    return current_user