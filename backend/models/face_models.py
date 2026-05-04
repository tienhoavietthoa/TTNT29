from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, LargeBinary, Text, func, UniqueConstraint
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class FaceEmbedding(Base):
    __tablename__ = "face_embedding"
    
    id_embedding = Column(Integer, primary_key=True, index=True)
    id_student = Column(Integer, ForeignKey("student.id_student"), nullable=False)
    id_class_attendance = Column(Integer, ForeignKey("class_attendance.id_class_attendance"), nullable=False)
    img_filename_embedding = Column(String(255))
    embedding_data = Column(LargeBinary)
    created_at_embedding = Column(DateTime, default=datetime.utcnow)
    notes_embedding = Column(Text)
    
    __table_args__ = (
        UniqueConstraint('id_student', 'id_class_attendance', name='unique_student_class'),
    )
    
    # Relationships
    student = relationship("Student", back_populates="face_embeddings")
    class_attendance = relationship("ClassAttendance", back_populates="face_embeddings")