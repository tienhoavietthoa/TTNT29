from sqlalchemy.orm import Session
from crud import class_crud, user_crud, auth_crud
from core.exceptions import (
    NotFoundException, ConflictException, BadRequestException
)
from datetime import datetime, date
import pandas as pd
from io import BytesIO

class ClassService:
    @staticmethod
    def get_classes_by_teacher(
        db: Session,
        id_account_teacher: int,
        id_course: int = None,
        id_faculty: int = None,
        status: str = None
    ):
        """Get teacher's classes with filters"""
        classes = class_crud.get_classes_by_teacher(
            db,
            id_account_teacher,
            id_course,
            id_faculty,
            status
        )
        
        return classes
    
    @staticmethod
    def get_class_info(db: Session, id_class_attendance: int):
        """Get detailed class information"""
        db_class = class_crud.get_class_attendance_by_id(db, id_class_attendance)
        if not db_class:
            raise NotFoundException("Class not found")
        
        # Get students in class
        students = class_crud.get_students_in_class(db, id_class_attendance)
        
        # Get sessions
        sessions = class_crud.get_sessions_by_class(db, id_class_attendance)
        
        return {
            "class": db_class,
            "students_count": len(students),
            "sessions_count": len(sessions),
            "students": students,
            "sessions": sessions
        }
    
    @staticmethod
    def import_classes_from_excel(
        db: Session,
        id_course: int,
        id_faculty: int,
        id_account_teacher: int,
        file_content: bytes
    ) -> dict:
        """Import classes from Excel"""
        try:
            df = pd.read_excel(BytesIO(file_content))
            
            new_classes = []
            duplicates = []
            
            for _, row in df.iterrows():
                code = str(row.get('code_class_attendance', '')).strip()
                name = str(row.get('name_class_attendance', '')).strip()
                total_students = int(row.get('total_students_class_attendance', 0))
                lesson_day = str(row.get('lesson_day_class_attendance', '')).strip()
                lesson_start_hour = row.get('lesson_start_hour', None)
                lesson_end_hour = row.get('lesson_end_hour', None)
                start_date = row.get('start_date_class_attendance', None)
                end_date = row.get('end_date_class_attendance', None)
                
                if not code or not name:
                    continue
                
                # Check if class already exists
                existing = class_crud.get_class_attendance_by_code(db, code)
                if existing:
                    duplicates.append(code)
                    continue
                
                db_class = class_crud.create_class_attendance(
                    db,
                    code_class_attendance=code,
                    name_class_attendance=name,
                    id_faculty=id_faculty,
                    id_course=id_course,
                    id_account_teacher=id_account_teacher,
                    total_students_class_attendance=total_students,
                    lesson_day_class_attendance=lesson_day,
                    lesson_start_hour=lesson_start_hour,
                    lesson_end_hour=lesson_end_hour,
                    start_date_class_attendance=start_date,
                    end_date_class_attendance=end_date
                )
                new_classes.append(db_class)
            
            return {
                "success": True,
                "imported": len(new_classes),
                "duplicates": duplicates,
                "message": f"Imported {len(new_classes)} classes"
            }
        except Exception as e:
            raise Exception(f"Error importing classes: {str(e)}")
    
    @staticmethod
    def add_students_to_class(
        db: Session,
        id_class_attendance: int,
        student_codes: List[str]
    ):
        """Add students to class"""
        db_class = class_crud.get_class_attendance_by_id(db, id_class_attendance)
        if not db_class:
            raise NotFoundException("Class not found")
        
        # Get current students count
        current_count = len(class_crud.get_students_in_class(db, id_class_attendance))
        
        added = []
        not_found = []
        already_in_class = []
        
        for code in student_codes:
            student = user_crud.get_student_by_code(db, code)
            if not student:
                not_found.append(code)
                continue
            
            # Check if already in class
            existing = db.query(class_crud.StudentClassAttendance).filter(
                class_crud.StudentClassAttendance.id_student == student.id_student,
                class_crud.StudentClassAttendance.id_class_attendance == id_class_attendance
            ).first()
            
            if existing:
                already_in_class.append(code)
                continue
            
            class_crud.add_student_to_class(db, student.id_student, id_class_attendance)
            added.append(code)
        
        return {
            "added": added,
            "not_found": not_found,
            "already_in_class": already_in_class,
            "total_students": current_count + len(added)
        }