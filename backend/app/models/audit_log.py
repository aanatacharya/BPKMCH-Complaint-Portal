from sqlalchemy import Column ,Integer, String, Enum, DateTime, Boolean, ForeignKey, func
from sqlalchemy.orm import relationship

from app.db.base import Base

class AuditLog(Base):
    
    __tablename__ = "audit_log"
    
    id = Column(Integer, primary_key=True, index=True)
    actor_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    action = Column(String(100), nullable=False)
    target_id = Column(Integer, nullable=False)
    target_type = Column(String(50), nullable=False)
    timestamp = Column(DateTime, server_default=func.now())
    
    actor = relationship("User")