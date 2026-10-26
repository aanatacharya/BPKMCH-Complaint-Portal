from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum, ForeignKey
from sqlalchemy import func
from sqlalchemy.orm import Relationship

from app.enums import Role
from app.db.base import Base

class User(Base):
    
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    unique_id = Column(String(50), unique=True, nullable=True) #Patient ID??
    mobile_number = Column(String(20), nullable=False)
    email = Column(String(255), unique=True, nullable=True)
    password_hash = Column(String(255), nullable=False)
    role = Column(Enum(Role), nullable=False, default=Role.user)
    is_mobile_verified = Column(Boolean, nullable=False, default=False)
    is_email_verified = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime, server_default=func.now())    
    department_id = Column(Integer, ForeignKey("departments.id"), nullable=True)
    
    department = Relationship("Department")

