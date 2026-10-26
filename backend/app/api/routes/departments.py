from fastapi import Depends, APIRouter, HTTPException, status
from sqlalchemy.orm import Session

from app.core.dependencies import require_superadmin
from app.models.user import User
from app.models.department import Department
from app.db.session import get_db
from app.crud.department import get_all_departments, create_department
from app.schemas.department import DepartmentOut, DepartmentCreate

router = APIRouter()

@router.get("/departments", response_model=list[DepartmentOut])
def list_department(db: Session = Depends(get_db)):
    return get_all_departments(db)

    
@router.post("/departments", response_model=DepartmentOut)
def new_department(department_in: DepartmentCreate, current_user: User = Depends(require_superadmin), db: Session = Depends(get_db)):
    existing = db.query(Department).filter(Department.name == department_in.name).first()
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Department already exists.")

    return create_department(db, department_in)
            

        
    