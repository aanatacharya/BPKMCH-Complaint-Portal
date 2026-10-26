from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.core.dependencies import require_superadmin
from app.models.user import User
from app.schemas.user import UserOut, AdminCreate
from app.schemas.complaint import ComplaintSuperAdminOut
from app.crud.complaint import get_all_complaints_for_super_admin, build_superadmin_complaints, get_complaint_by_id, get_private_complaints
from app.crud.user import get_user_by_username
from app.crud.audit_log import create_audit_log
from app.crud.user import create_admin

router = APIRouter()

@router.get("/superadmin/complaints", response_model=list[ComplaintSuperAdminOut])
def list_superadmin_complaint(current_user: User = Depends(require_superadmin), db: Session = Depends(get_db)):
    complaints = get_all_complaints_for_super_admin(db)
    return build_superadmin_complaints(db, complaints)

@router.get("/superadmin/complaints/{id}", response_model=ComplaintSuperAdminOut)
def get_superadmin_complaint(id: int, current_user: User = Depends(require_superadmin), db: Session = Depends(get_db)):
    complaint = get_complaint_by_id(db, id)
    
    if not complaint:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Complaints not found.")
    
    result = build_superadmin_complaints(db, [complaint])[0]
    
    create_audit_log(db, actor_id=current_user.id, action="viewed_named_complaint_identity", target_type="complaint", target_id=complaint.id)
    
    return result


@router.post("/superadmin/register-admin", response_model=UserOut)
def register_admin(admin_in: AdminCreate, current_user: User = Depends(require_superadmin), db: Session = Depends(get_db)):
    existing_user = get_user_by_username(db, admin_in.username)
    
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists.")
    
    new_admin = create_admin(db, admin_in)
    
    create_audit_log(db, actor_id=current_user.id, action="registered_new_admin", target_type="user", target_id=new_admin.id)
    
    return new_admin

@router.get("/superadmin/dashboard", response_model=list[ComplaintSuperAdminOut])
def get_superadmin_dashboard(current_user: User = Depends(require_superadmin), db: Session = Depends(get_db)):
    complaints = get_private_complaints(db)
    return build_superadmin_complaints(db, complaints)