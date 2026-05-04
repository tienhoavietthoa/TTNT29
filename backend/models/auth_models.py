from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class Level(Base):
    __tablename__ = "level"
    
    id_level = Column(Integer, primary_key=True, index=True)
    name_level = Column(String(20), unique=True, nullable=False)
    
    # Relationships
    logins = relationship("Login", back_populates="level")

class Login(Base):
    __tablename__ = "login"
    
    id_login = Column(Integer, primary_key=True, index=True)
    code_login = Column(String(50), unique=True, nullable=False)
    pass_login = Column(String(255), nullable=False)
    created_at_login = Column(DateTime, default=datetime.utcnow)
    id_level = Column(Integer, ForeignKey("level.id_level"), nullable=False)
    status_login = Column(String(20), default="OFF")  # OFF, ON, LOCKED
    
    # Relationships
    level = relationship("Level", back_populates="logins")
    account = relationship("Account", back_populates="login", uselist=False)
    sent_messages = relationship(
        "Message",
        foreign_keys="Message.sender_id_login",
        back_populates="sender"
    )
    received_messages = relationship(
        "Message",
        foreign_keys="Message.receiver_id_login",
        back_populates="receiver"
    )