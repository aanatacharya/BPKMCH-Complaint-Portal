from sqlalchemy import Column, Integer, String, Enum, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship

from app.db.base import Base
from app.enums import Visibility, IdentityDisplay

class Complaint(Base):
    __tablename__ = "complaints"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    department_id = Column(Integer, ForeignKey("departments.id"), nullable=False)
    description = Column(String(6000), nullable=False)
    visibility = Column(Enum(Visibility), nullable=False, default=Visibility.private)
    identity_display = Column(Enum(IdentityDisplay), nullable=False, default=IdentityDisplay.named)
    created_at = Column(DateTime, server_default=func.now())
    
    user = relationship("User")
    department = relationship("Department")
    