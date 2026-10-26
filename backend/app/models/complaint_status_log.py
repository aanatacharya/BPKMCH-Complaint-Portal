from sqlalchemy import Column, Integer, String, Enum, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship

from app.db.base import Base
from app.enums import ComplaintStatus

class ComplaintStatusLog(Base):
    __tablename__ = "complaint_status_log"
    
    id = Column(Integer, primary_key=True, index=True)
    complaint_id = Column(Integer, ForeignKey("complaints.id"), nullable=False)
    status = Column(Enum(ComplaintStatus), nullable=False)
    note = Column(String(1000), nullable=True)
    changed_at = Column(DateTime, server_default=func.now())
    changed_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    complaint = relationship("Complaint")
    changed_by_user = relationship("User")