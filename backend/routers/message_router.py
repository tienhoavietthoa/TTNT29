from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from services.message_service import MessageService
from core.dependencies import get_current_user
from models.auth_models import Login
from pydantic import BaseModel

router = APIRouter(prefix="/api/messages", tags=["messages"])

class MessageCreate(BaseModel):
    receiver_id_login: int
    content_message: str

@router.post("/send")
async def send_message(
    data: MessageCreate,
    current_user: Login = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Send message"""
    return MessageService.send_message(
        db, current_user.id_login, data.receiver_id_login, data.content_message
    )

@router.get("/conversation/{user_id}")
async def get_conversation(
    user_id: int,
    current_user: Login = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get conversation with another user"""
    return MessageService.get_conversation(db, current_user.id_login, user_id)

@router.get("/")
async def get_my_conversations(
    current_user: Login = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all my conversations"""
    return MessageService.get_user_conversations(db, current_user.id_login)