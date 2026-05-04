from sqlalchemy.orm import Session
from sqlalchemy import and_
from models.attendance_models import Attendance
from models.class_models import SessionAttendance
from datetime import datetime

def create_attendance(
    db: Session,
    id_session_attendance: int,
    id_student: int,
    id_class_attendance: int,
    status_attendance: str,
    checkin_time_attendance: datetime = None,
    img_filename_attendance: str = None,
    id_embedding: int = None,
    notes_attendance: str = None
) -> Attendance:
    """Create attendance record"""
    db_attendance = Attendance(
        id_session_attendance=id_session_attendance,
        id_student=id_student,
        id_class_attendance=id_class_attendance,
        status_attendance=status_attendance,
        checkin_time_attendance=checkin_time_attendance,
        img_filename_attendance=img_filename_attendance,
        id_embedding=id_embedding,
        notes_attendance=notes_attendance
    )
    db.add(db_attendance)
    db.commit()
    db.refresh(db_attendance)
    return db_attendance

def get_attendance_by_id(db: Session, id_attendance: int) -> Attendance:
    """Get attendance by id"""
    return db.query(Attendance).filter(
        Attendance.id_attendance == id_attendance
    ).first()

def get_attendance_by_session_and_student(
    db: Session,
    id_session_attendance: int,
    id_student: int
) -> Attendance:
    """Get attendance record by session and student"""
    return db.query(Attendance).filter(
        and_(
            Attendance.id_session_attendance == id_session_attendance,
            Attendance.id_student == id_student
        )
    ).first()

def get_attendances_by_session(db: Session, id_session_attendance: int):
    """Get all attendance records in a session"""
    return db.query(Attendance).filter(
        Attendance.id_session_attendance == id_session_attendance
    ).all()

def get_attendances_by_student_and_class(
    db: Session,
    id_student: int,
    id_class_attendance: int
):
    """Get all attendance records of a student in a class"""
    return db.query(Attendance).filter(
        and_(
            Attendance.id_student == id_student,
            Attendance.id_class_attendance == id_class_attendance
        )
    ).order_by(Attendance.created_at_attendance.desc()).all()

def update_attendance_status(
    db: Session,
    id_attendance: int,
    status_attendance: str,
    checkin_time_attendance: datetime = None,
    img_filename_attendance: str = None,
    notes_attendance: str = None
) -> Attendance:
    """Update attendance record"""
    db_attendance = get_attendance_by_id(db, id_attendance)
    if not db_attendance:
        return None
    
    db_attendance.status_attendance = status_attendance
    if checkin_time_attendance:
        db_attendance.checkin_time_attendance = checkin_time_attendance
    if img_filename_attendance:
        db_attendance.img_filename_attendance = img_filename_attendance
    if notes_attendance:
        db_attendance.notes_attendance = notes_attendance
    
    db.commit()
    db.refresh(db_attendance)
    return db_attendance

def update_attendance_manual(
    db: Session,
    id_attendance: int,
    notes_attendance: str
) -> Attendance:
    """Update attendance as manual"""
    return update_attendance_status(
        db,
        id_attendance,
        "manual",
        notes_attendance=notes_attendance
    )

def get_attendance_stats_by_session(db: Session, id_session_attendance: int):
    """Get attendance stats for a session"""
    total = db.query(Attendance).filter(
        Attendance.id_session_attendance == id_session_attendance
    ).count()
    
    present = db.query(Attendance).filter(
        and_(
            Attendance.id_session_attendance == id_session_attendance,
            Attendance.status_attendance.in_(["present", "manual"])
        )
    ).count()
    
    absent = total - present
    
    return {
        "total": total,
        "present": present,
        "absent": absent
    }

def get_student_absence_count(
    db: Session,
    id_student: int,
    id_class_attendance: int
) -> int:
    """Get number of absences for a student in a class"""
    return db.query(Attendance).filter(
        and_(
            Attendance.id_student == id_student,
            Attendance.id_class_attendance == id_class_attendance,
            Attendance.status_attendance == "absent"
        )
    ).count()