from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class ContactCreate(BaseModel):
    sender_name_contact: str
    user_type_contact: str  # teacher, student, other
    email_contact: EmailStr
    phone_contact: Optional[str]
    content_contact: str

class ContactResponse(BaseModel):
    id_contact: int
    sender_name_contact: str
    user_type_contact: str
    email_contact: str
    phone_contact: Optional[str]
    content_contact: str
    created_at_contact: datetime
    
    class Config:
        from_attributes = True