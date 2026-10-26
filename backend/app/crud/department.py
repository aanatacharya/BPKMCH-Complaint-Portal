from sqlalchemy.orm import Session

from app.models.department import Department
from app.schemas.department import DepartmentCreate

def get_all_departments(db: Session) -> list[Department]:
    return db.query(Department).all()

def get_department_by_id(db: Session, department_id: int) -> Department | None:
    return db.query(Department).filter(Department.id == department_id).first()

def create_department(db: Session, department_in: DepartmentCreate) -> Department:
    
    new_department = Department(
        name=department_in.name
    )
    
    db.add(new_department)
    db.commit()
    db.refresh(new_department)
    return new_department
