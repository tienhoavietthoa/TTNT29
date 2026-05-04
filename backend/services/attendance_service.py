from sqlalchemy.orm import Session
from crud import attendance_crud, class_crud
from core.exceptions import (
    NotFoundException, ConflictException, BadRequestException
)
from datetime import datetime, date, timedelta

class AttendanceService:
    @staticmethod
    def get_today_session(
        db: Session,
        id_class_attendance: int
    ):
        """Get today's session if exists"""
        sessions = class_crud.get_sessions_by_class(db, id_class_attendance)
        today = date.today()
        
        for session in sessions:
            if session.session_date == today:
                return session
        
        return None
    
    @staticmethod
    def checkin_student(
        db: Session,
        id_session_attendance: int,
        id_student: int,
        id_class_attendance: int,
        img_filename: str = None,
        id_embedding: int = None
    ):
        """Check in student"""
        # Check if already checked in
        existing = attendance_crud.get_attendance_by_session_and_student(
            db, id_session_attendance, id_student
        )
        
        if existing and existing.status_attendance != "absent":
            raise ConflictException("Student already checked in this session")
        
        if existing:
            # Update existing record
            existing.status_attendance = "present"
            existing.checkin_time_attendance = datetime.utcnow()
            existing.img_filename_attendance = img_filename
            existing.id_embedding = id_embedding
            db.commit()
            db.refresh(existing)
            return existing
        else:
            # Create new record
            return attendance_crud.create_attendance(
                db,
                id_session_attendance=id_session_attendance,
                id_student=id_student,
                id_class_attendance=id_class_attendance,
                status_attendance="present",
                checkin_time_attendance=datetime.utcnow(),
                img_filename_attendance=img_filename,
                id_embedding=id_embedding
            )
    
    @staticmethod
    def manual_checkin_student(
        db: Session,
        id_session_attendance: int,
        id_student: int,
        id_class_attendance: int,
        notes: str
    ):
        """Manual check in student"""
        existing = attendance_crud.get_attendance_by_session_and_student(
            db, id_session_attendance, id_student
        )
        
        if existing:
            # Update existing
            return attendance_crud.update_attendance_manual(
                db, existing.id_attendance, notes
            )
        else:
            # Create new
            return attendance_crud.create_attendance(
                db,
                id_session_attendance=id_session_attendance,
                id_student=id_student,
                id_class_attendance=id_class_attendance,
                status_attendance="manual",
                notes_attendance=notes
            )
    
    @staticmethod
    def get_session_attendance_details(
        db: Session,
        id_session_attendance: int
    ):
        """Get detailed session attendance info"""
        session = class_crud.get_session_attendance_by_id(db, id_session_attendance)
        if not session:
            raise NotFoundException("Session not found")
        
        attendances = attendance_crud.get_attendances_by_session(db, id_session_attendance)
        
        stats = {
            "total": len(attendances),
            "present": sum(1 for a in attendances if a.status_attendance in ["present", "manual"]),
            "absent": sum(1 for a in attendances if a.status_attendance == "absent"),
            "not_checked": sum(1 for a in attendances if not a.status_attendance)
        }
        
        return {
            "session": session,
            "attendances": attendances,
            "stats": stats
        }
    
    @staticmethod
    def get_student_attendance_in_class(
        db: Session,
        id_student: int,
        id_class_attendance: int
    ):
        """Get all attendance records of student in class"""
        attendances = attendance_crud.get_attendances_by_student_and_class(
            db, id_student, id_class_attendance
        )
        
        absent_count = sum(1 for a in attendances if a.status_attendance == "absent")
        
        return {
            "total_sessions": len(attendances),
            "present": sum(1 for a in attendances if a.status_attendance in ["present", "manual"]),
            "absent": absent_count,
            "absent_count_for_warning": absent_count >= 3,
            "attendances": attendances
        }