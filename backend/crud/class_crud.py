from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from models.class_models import (
    ClassAttendance, SessionAttendance, StudentClassAttendance
)
from models.user_models import Student
from datetime import date, datetime

def create_class_attendance(
    db: Session,
    code_class_attendance: str,
    name_class_attendance: str,
    id_faculty: int,
    id_course: int,
    id_account_teacher: int,
    total_students_class_attendance: int,
    lesson_day_class_attendance: str,
    lesson_start_hour,
    lesson_end_hour,
    start_date_class_attendance: date,
    end_date_class_attendance: date
) -> ClassAttendance:
    """Create class attendance"""
    db_class = ClassAttendance(
        code_class_attendance=code_class_attendance,
        name_class_attendance=name_class_attendance,
        id_faculty=id_faculty,
        id_course=id_course,
        id_account_teacher=id_account_teacher,
        total_students_class_attendance=total_students_class_attendance,
        lesson_day_class_attendance=lesson_day_class_attendance,
        lesson_start_hour=lesson_start_hour,
        lesson_end_hour=lesson_end_hour,
        start_date_class_attendance=start_date_class_attendance,
        end_date_class_attendance=end_date_class_attendance,
        status_class_attendance="ON"
    )
    db.add(db_class)
    db.commit()
    db.refresh(db_class)
    return db_class

def get_class_attendance_by_id(
    db: Session,
    id_class_attendance: int
) -> ClassAttendance:
    """Get class attendance by id"""
    return db.query(ClassAttendance).filter(
        ClassAttendance.id_class_attendance == id_class_attendance
    ).first()

def get_class_attendance_by_code(
    db: Session,
    code_class_attendance: str
) -> ClassAttendance:
    """Get class attendance by code"""
    return db.query(ClassAttendance).filter(
        ClassAttendance.code_class_attendance == code_class_attendance
    ).first()

def get_classes_by_teacher(
    db: Session,
    id_account_teacher: int,
    id_course: int = None,
    id_faculty: int = None,
    status: str = None
):
    """Get all classes by teacher"""
    query = db.query(ClassAttendance).filter(
        ClassAttendance.id_account_teacher == id_account_teacher
    )
    
    if id_course:
        query = query.filter(ClassAttendance.id_course == id_course)
    
    if id_faculty:
        query = query.filter(ClassAttendance.id_faculty == id_faculty)
    
    if status:
        query = query.filter(ClassAttendance.status_class_attendance == status)
    
    return query.all()

def get_all_classes(
    db: Session,
    id_course: int = None,
    id_faculty: int = None,
    status: str = None
):
    """Get all classes with filters"""
    query = db.query(ClassAttendance)
    
    if id_course:
        query = query.filter(ClassAttendance.id_course == id_course)
    
    if id_faculty:
        query = query.filter(ClassAttendance.id_faculty == id_faculty)
    
    if status:
        query = query.filter(ClassAttendance.status_class_attendance == status)
    
    return query.all()

def update_class_attendance_status(
    db: Session,
    id_class_attendance: int,
    status: str
) -> ClassAttendance:
    """Update class attendance status"""
    db_class = get_class_attendance_by_id(db, id_class_attendance)
    if not db_class:
        return None
    db_class.status_class_attendance = status
    db.commit()
    db.refresh(db_class)
    return db_class

def update_class_total_students(
    db: Session,
    id_class_attendance: int,
    total_students: int
) -> ClassAttendance:
    """Update total students in class"""
    db_class = get_class_attendance_by_id(db, id_class_attendance)
    if not db_class:
        return None
    db_class.total_students_class_attendance = total_students
    db.commit()
    db.refresh(db_class)
    return db_class

def delete_class_attendance(db: Session, id_class_attendance: int) -> bool:
    """Delete class attendance"""
    db_class = get_class_attendance_by_id(db, id_class_attendance)
    if not db_class:
        return False
    db.delete(db_class)
    db.commit()
    return True

# Session Attendance
def create_session_attendance(
    db: Session,
    id_class_attendance: int,
    session_number: int,
    session_date: date,
    session_start_hour=None,
    session_end_hour=None,
    status_session: str = "chưa tới"
) -> SessionAttendance:
    """Create session attendance"""
    db_session = SessionAttendance(
        id_class_attendance=id_class_attendance,
        session_number=session_number,
        session_date=session_date,
        session_start_hour=session_start_hour,
        session_end_hour=session_end_hour,
        status_session=status_session
    )
    db.add(db_session)
    db.commit()
    db.refresh(db_session)
    return db_session

def get_session_attendance_by_id(
    db: Session,
    id_session_attendance: int
) -> SessionAttendance:
    """Get session attendance by id"""
    return db.query(SessionAttendance).filter(
        SessionAttendance.id_session_attendance == id_session_attendance
    ).first()

def get_sessions_by_class(
    db: Session,
    id_class_attendance: int
):
    """Get all sessions in class"""
    return db.query(SessionAttendance).filter(
        SessionAttendance.id_class_attendance == id_class_attendance
    ).order_by(SessionAttendance.session_date).all()

def update_session_status(
    db: Session,
    id_session_attendance: int,
    status: str
) -> SessionAttendance:
    """Update session status"""
    db_session = get_session_attendance_by_id(db, id_session_attendance)
    if not db_session:
        return None
    db_session.status_session = status
    db.commit()
    db.refresh(db_session)
    return db_session

# Student Class Attendance
def add_student_to_class(
    db: Session,
    id_student: int,
    id_class_attendance: int
) -> StudentClassAttendance:
    """Add student to class"""
    # Check if already exists
    existing = db.query(StudentClassAttendance).filter(
        and_(
            StudentClassAttendance.id_student == id_student,
            StudentClassAttendance.id_class_attendance == id_class_attendance
        )
    ).first()
    
    if existing:
        return existing
    
    db_student_class = StudentClassAttendance(
        id_student=id_student,
        id_class_attendance=id_class_attendance
    )
    db.add(db_student_class)
    db.commit()
    db.refresh(db_student_class)
    return db_student_class

def get_students_in_class(
    db: Session,
    id_class_attendance: int
):
    """Get all students in class"""
    return db.query(Student).join(
        StudentClassAttendance,
        StudentClassAttendance.id_student == Student.id_student
    ).filter(
        StudentClassAttendance.id_class_attendance == id_class_attendance
    ).all()

def remove_student_from_class(
    db: Session,
    id_student: int,
    id_class_attendance: int
) -> bool:
    """Remove student from class"""
    db_student_class = db.query(StudentClassAttendance).filter(
        and_(
            StudentClassAttendance.id_student == id_student,
            StudentClassAttendance.id_class_attendance == id_class_attendance
        )
    ).first()
    
    if not db_student_class:
        return False
    
    db.delete(db_student_class)
    db.commit()
    return True