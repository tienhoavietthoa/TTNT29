from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Date, Time, func
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class ClassAttendance(Base):
    __tablename__ = "class_attendance"
    
    id_class_attendance = Column(Integer, primary_key=True, index=True)
    code_class_attendance = Column(String(50), unique=True, nullable=False)
    name_class_attendance = Column(String(100), nullable=False)
    id_faculty = Column(Integer, ForeignKey("faculty.id_faculty"))
    id_course = Column(Integer, ForeignKey("course.id_course"))
    id_account_teacher = Column(Integer, ForeignKey("account.id_account"))
    total_students_class_attendance = Column(Integer, default=0)
    status_class_attendance = Column(String(10), default="ON")
    lesson_day_class_attendance = Column(String(10))  # Monday, Tuesday, ...
    lesson_start_hour = Column(Time)
    lesson_end_hour = Column(Time)
    start_date_class_attendance = Column(Date)
    end_date_class_attendance = Column(Date)
    
    # Relationships
    faculty = relationship("Faculty", back_populates="class_attendances")
    course = relationship("Course", back_populates="class_attendances")
    teacher = relationship("Account", back_populates="classes")
    sessions = relationship("SessionAttendance", back_populates="class_attendance")
    students = relationship("StudentClassAttendance", back_populates="class_attendance")
    attendances = relationship("Attendance", back_populates="class_attendance")
    face_embeddings = relationship("FaceEmbedding", back_populates="class_attendance")

class SessionAttendance(Base):
    __tablename__ = "session_attendance"
    
    id_session_attendance = Column(Integer, primary_key=True, index=True)
    id_class_attendance = Column(Integer, ForeignKey("class_attendance.id_class_attendance"))
    session_number = Column(Integer, nullable=False)
    session_date = Column(Date, nullable=False)
    session_start_hour = Column(Time)
    session_end_hour = Column(Time)
    status_session = Column(String(20))
    
    # Relationships
    class_attendance = relationship("ClassAttendance", back_populates="sessions")
    attendances = relationship("Attendance", back_populates="session")

class StudentClassAttendance(Base):
    __tablename__ = "student_class_attendance"
    
    id_student_class_attendance = Column(Integer, primary_key=True, index=True)
    id_student = Column(Integer, ForeignKey("student.id_student"))
    id_class_attendance = Column(Integer, ForeignKey("class_attendance.id_class_attendance"))
    
    # Relationships
    student = relationship("Student", back_populates="class_attendances")
    class_attendance = relationship("ClassAttendance", back_populates="students")
    