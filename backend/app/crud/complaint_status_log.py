from sqlalchemy.orm import Session

from app.models.complaint_status_log import ComplaintStatusLog
from app.enums import ComplaintStatus

def add_status_log(db: Session, complaint_id: int, status: ComplaintStatus, changed_by: int, note: str | None = None) -> ComplaintStatusLog:
    new_complaint_status_log = ComplaintStatusLog(
        complaint_id=complaint_id,
        status=status,
        note=note,
        changed_by=changed_by
    )
    db.add(new_complaint_status_log)
    db.commit()
    db.refresh(new_complaint_status_log)
    return new_complaint_status_log
    
def get_latest_status(db: Session, complaint_id: int) -> ComplaintStatusLog | None:
    return db.query(ComplaintStatusLog).filter(ComplaintStatusLog.complaint_id == complaint_id).order_by(ComplaintStatusLog.changed_at.desc()).first()

