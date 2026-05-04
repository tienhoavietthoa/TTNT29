from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from models.message_models import Message
from datetime import datetime

def create_message(
    db: Session,
    sender_id_login: int,
    receiver_id_login: int,
    content_message: str
) -> Message:
    """Create message"""
    db_message = Message(
        sender_id_login=sender_id_login,
        receiver_id_login=receiver_id_login,
        content_message=content_message
    )
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message

def get_message_by_id(db: Session, id_message: int) -> Message:
    """Get message by id"""
    return db.query(Message).filter(
        Message.id_message == id_message
    ).first()

def get_conversation(
    db: Session,
    user1_id: int,
    user2_id: int
):
    """Get conversation between two users"""
    return db.query(Message).filter(
        or_(
            and_(
                Message.sender_id_login == user1_id,
                Message.receiver_id_login == user2_id
            ),
            and_(
                Message.sender_id_login == user2_id,
                Message.receiver_id_login == user1_id
            )
        )
    ).order_by(Message.sent_at_message).all()

def get_messages_sent_by_user(db: Session, sender_id_login: int):
    """Get all messages sent by user"""
    return db.query(Message).filter(
        Message.sender_id_login == sender_id_login
    ).order_by(Message.sent_at_message.desc()).all()

def get_messages_received_by_user(db: Session, receiver_id_login: int):
    """Get all messages received by user"""
    return db.query(Message).filter(
        Message.receiver_id_login == receiver_id_login
    ).order_by(Message.sent_at_message.desc()).all()

def get_user_conversations(db: Session, user_id: int):
    """Get all unique conversations for a user"""
    messages = db.query(Message).filter(
        or_(
            Message.sender_id_login == user_id,
            Message.receiver_id_login == user_id
        )
    ).order_by(Message.sent_at_message.desc()).all()
    
    conversations = {}
    for msg in messages:
        other_user_id = msg.receiver_id_login if msg.sender_id_login == user_id else msg.sender_id_login
        if other_user_id not in conversations:
            conversations[other_user_id] = msg
    
    return conversations