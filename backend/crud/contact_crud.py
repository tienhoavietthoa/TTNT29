from sqlalchemy.orm import Session
from models.contact_models import Contact
from datetime import datetime

def create_contact(
    db: Session,
    sender_name_contact: str,
    user_type_contact: str,
    email_contact: str,
    phone_contact: str,
    content_contact: str
) -> Contact:
    """Create contact form submission"""
    db_contact = Contact(
        sender_name_contact=sender_name_contact,
        user_type_contact=user_type_contact,
        email_contact=email_contact,
        phone_contact=phone_contact,
        content_contact=content_contact
    )
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact

def get_contact_by_id(db: Session, id_contact: int) -> Contact:
    """Get contact by id"""
    return db.query(Contact).filter(
        Contact.id_contact == id_contact
    ).first()

def get_all_contacts(db: Session):
    """Get all contacts"""
    return db.query(Contact).order_by(
        Contact.created_at_contact.desc()
    ).all()

def get_contacts_by_type(db: Session, user_type_contact: str):
    """Get contacts by type"""
    return db.query(Contact).filter(
        Contact.user_type_contact == user_type_contact
    ).order_by(Contact.created_at_contact.desc()).all()