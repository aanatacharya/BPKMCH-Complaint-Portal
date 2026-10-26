from sqlalchemy.orm import Session
from datetime import datetime

from app.models.otp_verification import OtpVerification
from app.enums import OtpChannel

def create_otp(db: Session, user_id: int, channel: OtpChannel, code_hash: str, expires_at: datetime) -> OtpVerification:
    new_otp_verification = OtpVerification(
        user_id=user_id,
        channel=channel,
        code_hash=code_hash,
        expires_at=expires_at
    )
    db.add(new_otp_verification)
    db.commit()
    db.refresh(new_otp_verification)
    
    return new_otp_verification

def get_latest_otp(db: Session, user_id: int, channel: OtpChannel) -> OtpVerification | None:
    return db.query(OtpVerification).filter(OtpVerification.user_id == user_id, OtpVerification.channel == channel).order_by(OtpVerification.created_at.desc()).first()

def mark_otp_used(db: Session, otp: OtpVerification) -> OtpVerification:
    otp.is_used = True
    db.commit()
    db.refresh(otp)
    return otp
