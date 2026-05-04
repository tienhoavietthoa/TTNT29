from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class MessageCreate(BaseModel):
    receiver_id_login: int
    content_message: str

class MessageResponse(BaseModel):
    id_message: int
    sender_id_login: int
    receiver_id_login: int
    content_message: str
    sent_at_message: datetime
    
    class Config:
        from_attributes = True