from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, func, UniqueConstraint
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class Attendance(Base):
    __tablename__ = "attendance"
    
    id_attendance = Column(Integer, primary_key=True, index=True)
    id_session_attendance = Column(Integer, ForeignKey("session_attendance.id_session_attendance"), nullable=False)
    id_student = Column(Integer, ForeignKey("student.id_student"), nullable=False)
    id_class_attendance = Column(Integer, ForeignKey("class_attendance.id_class_attendance"), nullable=False)
    status_attendance = Column(String(20), nullable=False)  # present, absent, manual
    checkin_time_attendance = Column(DateTime)
    img_filename_attendance = Column(String(255))
    id_embedding = Column(Integer, ForeignKey("face_embedding.id_embedding"))
    notes_attendance = Column(Text)
    created_at_attendance = Column(DateTime, default=datetime.utcnow)
    
    __table_args__ = (
        UniqueConstraint('id_session_attendance', 'id_student', name='unique_session_student'),
    )
    
    # Relationships
    session = relationship("SessionAttendance", back_populates="attendances")
    student = relationship("Student", back_populates="attendances")
    class_attendance = relationship("ClassAttendance", back_populates="attendances")