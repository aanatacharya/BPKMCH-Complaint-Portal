from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.models.complaint import Complaint
from app.models.complaint_status_log import ComplaintStatusLog
from app.schemas.complaint import ComplaintCreate, ComplaintOut, ComplaintPublicOut, ComplaintAdminOut, ComplaintSuperAdminOut
from app.enums import ComplaintStatus, Visibility, IdentityDisplay
from app.crud.complaint_status_log import get_latest_status
from app.models.user import User

def create_complaint(db: Session, complaint_in: ComplaintCreate, user_id: int) -> Complaint:
    
    new_complaint = Complaint(
        user_id=user_id,
        department_id=complaint_in.department_id,
        description=complaint_in.description,
        visibility=complaint_in.visibility,
        identity_display=complaint_in.identity_display
    )
    
    db.add(new_complaint)
    db.commit()
    db.refresh(new_complaint)
    
    return new_complaint

def get_complaint_by_id(db: Session, complaint_id: int) -> Complaint | None:
    return db.query(Complaint).filter(Complaint.id == complaint_id).first()

def get_complaints_for_user(db: Session, user_id: int) -> list[Complaint]:
    return db.query(Complaint).filter(Complaint.user_id == user_id).all()

def get_public_complaints(db: Session, skip: int = 0, limit: int = 20) -> list[Complaint]:
    return db.query(Complaint).filter(Complaint.visibility == Visibility.public).offset(skip).limit(limit).all()

def get_complaints_for_admin(db: Session, department_id: int) -> list[Complaint]:
    return db.query(Complaint).filter( or_(Complaint.department_id == department_id, Complaint.visibility == Visibility.public)).all()

def get_all_complaints_for_super_admin(db: Session) -> list[Complaint]:
    return db.query(Complaint).all()

def get_complaint_with_status(db: Session, complaint: Complaint) -> ComplaintOut:
    status_log = get_latest_status(db, complaint.id)
    
    current_status = status_log.status if status_log else ComplaintStatus.pending
    
    return ComplaintOut(
        id=complaint.id,
        department_id=complaint.department_id,
        description=complaint.description,
        visibility=complaint.visibility,
        identity_display=complaint.identity_display,
        created_at=complaint.created_at,
        current_status=current_status,
    )

def get_complaints_with_status(db: Session, complaints: list[Complaint]) -> list[ComplaintOut]:
    return [get_complaint_with_status(db, complaint) for complaint in complaints]

def build_public_complaints(db: Session, complaints: list[Complaint]) -> list[ComplaintPublicOut]:
    results = []

    for complaint in complaints:
        status_log = get_latest_status(db, complaint.id)
        current_status = status_log.status if status_log else ComplaintStatus.pending

        if complaint.identity_display == IdentityDisplay.named:
            filer_username = complaint.user.username
        else:
            filer_username = None

        results.append(
            ComplaintPublicOut(
                id=complaint.id,
                department_id=complaint.department_id,
                description=complaint.description,
                visibility=complaint.visibility,
                identity_display=complaint.identity_display,
                created_at=complaint.created_at,
                current_status=current_status,
                filer_username=filer_username,
            )
        )

    return results
        

def build_admin_complaints(db: Session, complaints: list[Complaint]) -> list[ComplaintAdminOut]:
    results = []

    for complaint in complaints:
        status_log = get_latest_status(db, complaint.id)
        current_status = status_log.status if status_log else ComplaintStatus.pending

        if complaint.identity_display == IdentityDisplay.named:
            filer_username = complaint.user.username
        else:
            filer_username = None

        results.append(
            ComplaintAdminOut(
                id=complaint.id,
                department_id=complaint.department_id,
                description=complaint.description,
                visibility=complaint.visibility,
                identity_display=complaint.identity_display,
                created_at=complaint.created_at,
                current_status=current_status,
                filer_username=filer_username,
            )
        )

    return results

def build_superadmin_complaints(db: Session, complaints: list[Complaint]) -> list[ComplaintSuperAdminOut]:
    results = []

    for complaint in complaints:
        status_log = get_latest_status(db, complaint.id)
        current_status = status_log.status if status_log else ComplaintStatus.pending

        results.append(
            ComplaintSuperAdminOut(
                id=complaint.id,
                department_id=complaint.department_id,
                description=complaint.description,
                visibility=complaint.visibility,
                identity_display=complaint.identity_display,
                created_at=complaint.created_at,
                current_status=current_status,
                filer_username=complaint.user.username,
            )
        )

    return results


def get_department_complaints(db: Session, department_id: int) -> list[Complaint]:
    return db.query(Complaint).filter(Complaint.department_id == department_id).all()

def get_private_complaints(db: Session) -> list[Complaint]:
    return db.query(Complaint).filter(Complaint.visibility == Visibility.private).all()

def search_department_complaints_by_filer(db: Session, department_id: int, filer_name: str) -> list[Complaint]:
    return db.query(Complaint).join(User, Complaint.user_id == User.id).filter(
        Complaint.department_id == department_id,
        User.username.ilike(f"%{filer_name}%")
    ).all()