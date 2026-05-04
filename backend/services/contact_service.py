from sqlalchemy.orm import Session
from crud import contact_crud
from services.auth_service import AuthService

class ContactService:
    @staticmethod
    def create_contact(
        db: Session,
        sender_name_contact: str,
        user_type_contact: str,
        email_contact: str,
        phone_contact: str,
        content_contact: str
    ):
        """Create contact form submission"""
        contact = contact_crud.create_contact(
            db,
            sender_name_contact=sender_name_contact,
            user_type_contact=user_type_contact,
            email_contact=email_contact,
            phone_contact=phone_contact,
            content_contact=content_contact
        )
        
        # Send confirmation email
        AuthService._send_email(
            email_contact,
            "Cảm ơn bạn đã liên hệ - Hệ thống Điểm Danh",
            f"Xin chào {sender_name_contact},\n\nCảm ơn bạn đã gửi liên hệ. Chúng tôi sẽ phản hồi sớm nhất.\n\nBest regards,\nHệ thống Điểm Danh"
        )
        
        return contact
    
    @staticmethod
    def get_all_contacts(db: Session):
        """Get all contacts for admin"""
        return contact_crud.get_all_contacts(db)