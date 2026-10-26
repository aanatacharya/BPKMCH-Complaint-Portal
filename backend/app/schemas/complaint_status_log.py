from pydantic import BaseModel ,ConfigDict
from typing import Optional
from datetime import datetime

from app.enums import ComplaintStatus

class StatusUpdateRequest(BaseModel):
    status : ComplaintStatus
    note : Optional[str] = None

class StatusLogOut(BaseModel):
    id : int
    complaint_id : int
    status : ComplaintStatus
    changed_by : int
    note : Optional[str]
    changed_at: datetime
    model_config = ConfigDict(from_attributes=True)