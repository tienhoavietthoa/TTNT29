from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Date, func
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class Course(Base):
    __tablename__ = "course"
    
    id_course = Column(Integer, primary_key=True, index=True)
    start_year_course = Column(Integer, nullable=False)
    end_year_course = Column(Integer, nullable=False)
    name_course = Column(String(20), unique=True, nullable=False)
    
    # Relationships
    faculties = relationship("Faculty", back_populates="course")
    class_admins = relationship("ClassAdmin", back_populates="course")
    class_attendances = relationship("ClassAttendance", back_populates="course")

class Faculty(Base):
    __tablename__ = "faculty"
    
    id_faculty = Column(Integer, primary_key=True, index=True)
    fullname_faculty = Column(String(100), nullable=False)
    shortname_faculty = Column(String(20), nullable=False)
    id_course = Column(Integer, ForeignKey("course.id_course"))
    
    # Relationships
    course = relationship("Course", back_populates="faculties")
    class_admins = relationship("ClassAdmin", back_populates="faculty")
    class_attendances = relationship("ClassAttendance", back_populates="faculty")

class ClassAdmin(Base):
    __tablename__ = "class_admin"
    
    id_class_admin = Column(Integer, primary_key=True, index=True)
    name_class_admin = Column(String(50), nullable=False)
    id_faculty = Column(Integer, ForeignKey("faculty.id_faculty"))
    id_course = Column(Integer, ForeignKey("course.id_course"))
    
    # Relationships
    faculty = relationship("Faculty", back_populates="class_admins")
    course = relationship("Course", back_populates="class_admins")
    students = relationship("Student", back_populates="class_admin")

class Account(Base):
    __tablename__ = "account"
    
    id_account = Column(Integer, primary_key=True, index=True)
    name_account = Column(String(100), nullable=False)
    email_account = Column(String(200), unique=True, nullable=False)
    phone_account = Column(String(20))
    id_login = Column(Integer, ForeignKey("login.id_login", ondelete="CASCADE"), unique=True)
    
    # Relationships
    login = relationship("Login", back_populates="account")
    classes = relationship("ClassAttendance", back_populates="teacher")

class Student(Base):
    __tablename__ = "student"
    
    id_student = Column(Integer, primary_key=True, index=True)
    code_student = Column(String(50), unique=True, nullable=False)
    name_student = Column(String(100), nullable=False)
    email_student = Column(String(200))
    phone_student = Column(String(20))
    dob_student = Column(Date)
    id_class_admin = Column(Integer, ForeignKey("class_admin.id_class_admin"))
    status_student = Column(String(10), default="ON")
    created_at_student = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    class_admin = relationship("ClassAdmin", back_populates="students")
    class_attendances = relationship("StudentClassAttendance", back_populates="student")
    attendances = relationship("Attendance", back_populates="student")
    face_embeddings = relationship("FaceEmbedding", back_populates="student")