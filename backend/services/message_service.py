from sqlalchemy.orm import Session
from crud import message_crud, auth_crud
from core.exceptions import NotFoundException

class MessageService:
    @staticmethod
    def send_message(
        db: Session,
        sender_id_login: int,
        receiver_id_login: int,
        content_message: str
    ):
        """Send message"""
        # Verify both users exist
        sender = auth_crud.get_login_by_id(db, sender_id_login)
        receiver = auth_crud.get_login_by_id(db, receiver_id_login)
        
        if not sender or not receiver:
            raise NotFoundException("User not found")
        
        return message_crud.create_message(
            db, sender_id_login, receiver_id_login, content_message
        )
    
    @staticmethod
    def get_conversation(db: Session, user1_id: int, user2_id: int):
        """Get conversation between two users"""
        return message_crud.get_conversation(db, user1_id, user2_id)
    
    @staticmethod
    def get_user_conversations(db: Session, user_id: int):
        """Get all conversations for a user"""
        return message_crud.get_user_conversations(db, user_id)