from fastapi import Depends, APIRouter, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.user import User
from app.schemas.complaint import ComplaintCreate, ComplaintOut, ComplaintPublicOut
from app.crud.complaint import create_complaint
from app.core.dependencies import get_current_user
from app.crud.complaint_status_log import add_status_log
from app.enums import ComplaintStatus
from app.crud.complaint import get_complaints_for_user, get_complaint_with_status, get_complaints_with_status, get_public_complaints, build_public_complaints, get_complaint_by_id



router = APIRouter()

@router.post("/complaints", response_model=ComplaintOut)
def file_complaint(complaint_in: ComplaintCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    new_complaint = create_complaint(db, complaint_in, current_user.id)
    add_status_log(db, new_complaint.id, ComplaintStatus.pending, current_user.id)
    return get_complaint_with_status(db, new_complaint)

@router.get("/complaints/me", response_model=list[ComplaintOut])
def get_my_complaints(current_user : User = Depends(get_current_user), db: Session = Depends(get_db)):
    complaints = get_complaints_for_user(db, current_user.id)
    return get_complaints_with_status(db, complaints)

@router.get("/complaints/public", response_model=list[ComplaintPublicOut])
def list_public_complaints(skip: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    complaints = get_public_complaints(db, skip, limit)
    return build_public_complaints(db, complaints)

@router.get("/complaints/{id}",  response_model=ComplaintOut)
def get_complaint(id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    
    complaint = get_complaint_by_id(db, id)
    
    if not complaint:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Complaint not found.")
    
    if complaint.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You do not have access to this complaint.")
    
    return get_complaint_with_status(db, complaint)