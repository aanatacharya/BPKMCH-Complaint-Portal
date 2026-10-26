from sqlalchemy.orm import Session

from app.models.audit_log import AuditLog

def create_audit_log(db: Session, actor_id: int, action: str, target_type: str, target_id: int) -> AuditLog:
    new_audit_log = AuditLog(
        actor_id=actor_id,
        action=action,
        target_id=target_id,
        target_type=target_type
    )

    db.add(new_audit_log)
    db.commit()
    db.refresh(new_audit_log)
    return new_audit_log

def get_logs_for_target(db: Session, target_type: str, target_id: int) -> list[AuditLog]:
    return db.query(AuditLog).filter(
        AuditLog.target_type == target_type,
        AuditLog.target_id == target_id
    ).all()

def get_logs_by_actor(db: Session, actor_id: int) -> list[AuditLog]:
    return db.query(AuditLog).filter(AuditLog.actor_id == actor_id).all()