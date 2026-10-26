from pydantic import BaseModel, ConfigDict
from datetime import datetime

from app.enums import OtpChannel

class OtpOut(BaseModel):
    id: int
    user_id: int
    channel: OtpChannel
    expires_at: datetime
    is_used: bool
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)