from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.user import UserCreate, AdminCreate
from app.core.security import hash_password
from app.enums import Role

def create_user(db: Session, user_in: UserCreate) -> User:
    hashed_pw = hash_password(user_in.password)
    
    new_user = User(
        username=user_in.username,
        mobile_number=user_in.mobile_number,
        password_hash=hashed_pw,
        unique_id=user_in.unique_id,
        email=user_in.email
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def create_admin(db: Session, admin_in: AdminCreate) -> User:
    hashed_pw = hash_password(admin_in.password)
    
    new_admin = User(
        username=admin_in.username,
        mobile_number=admin_in.mobile_number,
        password_hash=hashed_pw,
        unique_id=admin_in.unique_id,
        email=admin_in.email,
        role=Role.admin,
        department_id=admin_in.department_id
    )
    
    db.add(new_admin)
    db.commit()
    db.refresh(new_admin)
    return new_admin

def get_user_by_username(db: Session, username: str) -> User | None:
    return db.query(User).filter(User.username == username).first()

def get_user_by_id(db: Session, id: int) -> User | None:
    return db.query(User).filter(User.id == id).first()
    