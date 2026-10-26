from pydantic import BaseModel, ConfigDict

class DepartmentOut(BaseModel):
    id: int
    name: str
    
    model_config = ConfigDict(from_attributes=True)

class DepartmentCreate(BaseModel):
    name: str