from sqlalchemy import Column ,Integer, String, Enum, DateTime, Boolean, ForeignKey, func
from sqlalchemy.orm import relationship

from app.enums import OtpChannel
from app.db.base import Base

class OtpVerification(Base):
    __tablename__ = "otp_verifications"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    channel = Column(Enum(OtpChannel), nullable=False)
    code_hash = Column(String(255), nullable=False)
    expires_at = Column(DateTime, nullable=False)
    is_used = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime, server_default=func.now())
    
    user = relationship("User")
