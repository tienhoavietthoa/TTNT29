from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class LevelResponse(BaseModel):
    id_level: int
    name_level: str
    
    class Config:
        from_attributes = True

class LoginRegister(BaseModel):
    code_login: str
    name_account: str
    email_account: EmailStr
    phone_account: Optional[str] = None
    password: str
    confirm_password: str

class LoginRequest(BaseModel):
    code_login: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class RefreshTokenRequest(BaseModel):
    refresh_token: str

class ChangePasswordRequest(BaseModel):
    old_password: str
    new_password: str
    confirm_password: str

class LoginResponse(BaseModel):
    id_login: int
    code_login: str
    status_login: str
    level: LevelResponse
    
    class Config:
        from_attributes = True

class UserMeResponse(BaseModel):
    id_account: int
    name_account: str
    email_account: str
    phone_account: Optional[str]
    login: LoginResponse
    
    class Config:
        from_attributes = True