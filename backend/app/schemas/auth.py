from pydantic import BaseModel

class LoginRequest(BaseModel):
    username : str
    password : str

class TokenResponse(BaseModel):
    access_token : str
    refresh_token : str
    token_type : str = "bearer"
    
class OtpVerifyRequest(BaseModel):
    user_id : int
    code : str
    
class RefreshTokenRequest(BaseModel):
    refresh_token : str
    