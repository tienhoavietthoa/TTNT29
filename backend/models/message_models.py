from sqlalchemy import Column, Integer, Text, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class Message(Base):
    __tablename__ = "message"
    
    id_message = Column(Integer, primary_key=True, index=True)
    sender_id_login = Column(Integer, ForeignKey("login.id_login"), nullable=False)
    receiver_id_login = Column(Integer, ForeignKey("login.id_login"), nullable=False)
    content_message = Column(Text, nullable=False)
    sent_at_message = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    sender = relationship("Login", foreign_keys=[sender_id_login], back_populates="sent_messages")
    receiver = relationship("Login", foreign_keys=[receiver_id_login], back_populates="received_messages")