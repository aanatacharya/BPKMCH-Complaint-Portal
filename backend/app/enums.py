from enum import Enum

class Role(Enum):
    user = "user"
    admin = "admin" #HOD
    superadmin = "superadmin" 
    
class Visibility(Enum):
    public = "public"
    private = "private"

class IdentityDisplay(Enum):
    named = "named"
    anonymous = "anonymous"
    
class ComplaintStatus(Enum):
    pending = "pending"
    under_review = "under_review"
    resolved = "resolved"
    rejected = "rejected"

class OtpChannel(str, Enum):
    mobile = "mobile"
    email = "email"
    
