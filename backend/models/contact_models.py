from sqlalchemy import Column, Integer, String, DateTime, Text, func
from datetime import datetime
from database import Base

class Contact(Base):
    __tablename__ = "contact"
    
    id_contact = Column(Integer, primary_key=True, index=True)
    sender_name_contact = Column(String(100), nullable=False)
    user_type_contact = Column(String(20), nullable=False)  # teacher, student, other
    email_contact = Column(String(200), nullable=False)
    phone_contact = Column(String(20))
    content_contact = Column(Text, nullable=False)
    created_at_contact = Column(DateTime, default=datetime.utcnow)