from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.core.dependencies import require_admin
from app.models.user import User
from app.schemas.complaint import ComplaintAdminOut
from app.crud.complaint import build_admin_complaints, get_complaints_for_admin, get_complaint_by_id
from app.crud.audit_log import create_audit_log
from app.crud.complaint import get_department_complaints, search_department_complaints_by_filer
from app.schemas.complaint_status_log import StatusUpdateRequest, StatusLogOut
from app.crud.complaint_status_log import add_status_log
from app.enums import Role, Visibility, IdentityDisplay

router = APIRouter()


@router.get("/admin/complaints", response_model=list[ComplaintAdminOut])
def list_admin_complaints(current_user: User = Depends(require_admin), db: Session = Depends(get_db)):
    if current_user.role == Role.admin and current_user.department_id is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Your admin account has no department assigned. Contact a superadmin."
        )

    complaints = get_complaints_for_admin(db, current_user.department_id)
    return build_admin_complaints(db, complaints)


@router.get("/admin/complaints/{id}", response_model=ComplaintAdminOut)
def get_admin_complaint(id: int, current_user: User = Depends(require_admin), db: Session = Depends(get_db)):
    complaint = get_complaint_by_id(db, id)

    if not complaint:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Complaint not found.")

    if current_user.role == Role.admin:
        if current_user.department_id is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Your admin account has no department assigned.")

        is_own_department = complaint.department_id == current_user.department_id
        is_public = complaint.visibility == Visibility.public

        if not (is_own_department or is_public):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You do not have access to this complaint.")

    result = build_admin_complaints(db, [complaint])[0]

    if complaint.identity_display == IdentityDisplay.named:
        create_audit_log(db, actor_id=current_user.id, action="viewed_named_complaint_identity", target_type="complaint", target_id=complaint.id)

    return result


@router.post("/admin/complaints/{id}/status", response_model=StatusLogOut)
def update_complaint_status(id: int, status_in: StatusUpdateRequest, current_user: User = Depends(require_admin), db: Session = Depends(get_db)):
    complaint = get_complaint_by_id(db, id)

    if not complaint:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Complaint not found.")

    if current_user.role == Role.admin:
        if current_user.department_id is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Your admin account has no department assigned.")

        if complaint.department_id != current_user.department_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You can only update complaints in your own department.")

    new_log = add_status_log(db, complaint_id=complaint.id, status=status_in.status, changed_by=current_user.id, note=status_in.note)

    create_audit_log(db, actor_id=current_user.id, action="status_changed", target_type="complaint", target_id=complaint.id)

    return new_log


@router.get("/admin/dashboard", response_model=list[ComplaintAdminOut])
def get_admin_dashboard(current_user: User = Depends(require_admin), db: Session = Depends(get_db)):
    if current_user.role == Role.admin and current_user.department_id is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Your admin account has no department assigned. Contact a superadmin."
        )

    complaints = get_department_complaints(db, current_user.department_id)
    return build_admin_complaints(db, complaints)

@router.get("/admin/complaints/search", response_model=list[ComplaintAdminOut])
def search_complaints(filer_name: str, current_user: User = Depends(require_admin), db: Session = Depends(get_db)):
    if current_user.role == Role.admin and current_user.department_id is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Your admin account has no department assigned.")

    complaints = search_department_complaints_by_filer(db, current_user.department_id, filer_name)
    return build_admin_complaints(db, complaints)

