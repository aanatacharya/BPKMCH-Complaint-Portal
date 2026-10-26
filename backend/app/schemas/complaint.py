from pydantic import BaseModel, ConfigDict, Field
from typing import Optional
from datetime import datetime

from app.enums import Visibility, IdentityDisplay, ComplaintStatus

class ComplaintCreate(BaseModel):
    department_id : int
    description : str = Field(max_length=6000)
    visibility : Visibility
    identity_display : IdentityDisplay

class ComplaintOut(BaseModel):
    id : int
    department_id : int
    description : str
    visibility : Visibility
    identity_display : IdentityDisplay
    created_at : datetime
    current_status: ComplaintStatus
    
    model_config = ConfigDict(from_attributes=True)
    
class ComplaintAdminOut(BaseModel):
    id : int
    department_id : int
    description : str
    visibility : Visibility
    identity_display : IdentityDisplay
    filer_username : Optional[str] = None
    created_at : datetime
    current_status : ComplaintStatus
    
    model_config = ConfigDict(from_attributes=True)
    
class ComplaintPublicOut(BaseModel):
    id : int
    department_id : int
    description : str
    visibility : Visibility
    identity_display : IdentityDisplay
    filer_username : Optional[str] = None
    created_at : datetime
    current_status : ComplaintStatus
        
    model_config = ConfigDict(from_attributes=True)

class ComplaintSuperAdminOut(BaseModel):
    id : int
    department_id : int
    description : str
    visibility : Visibility
    identity_display : IdentityDisplay
    filer_username : str
    created_at : datetime
    current_status : ComplaintStatus
        
    model_config = ConfigDict(from_attributes=True)
    
    
    