from pydantic import BaseModel, ConfigDict
from typing import Optional

from app.enums import Role

class UserCreate(BaseModel):
    username : str
    mobile_number : str
    password : str
    unique_id : Optional[str] = None
    email : Optional[str] = None
    
class UserOut(BaseModel):
    id : int
    username : str
    mobile_number : str
    unique_id : Optional[str]
    email : Optional[str]
    role : Role
    is_mobile_verified : bool
    is_email_verified : bool
    department_id: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)

class AdminCreate(UserCreate):
    department_id : int
    

