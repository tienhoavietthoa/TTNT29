from sqlalchemy.orm import Session
from crud import user_crud, auth_crud, class_crud
from models.user_models import Student, Account
from core.exceptions import NotFoundException, ConflictException
from typing import List
import pandas as pd
from io import BytesIO

class UserService:
    @staticmethod
    def get_teacher_profile(db: Session, id_account: int):
        """Get teacher profile"""
        account = auth_crud.get_account_by_id(db, id_account)
        if not account:
            raise NotFoundException("Account not found")
        
        return {
            "id_account": account.id_account,
            "name": account.name_account,
            "email": account.email_account,
            "phone": account.phone_account
        }
    
    @staticmethod
    def import_students_from_excel(
        db: Session,
        id_course: int,
        id_faculty: int,
        id_class_admin: int,
        file_content: bytes
    ) -> dict:
        """Import students from Excel file"""
        try:
            df = pd.read_excel(BytesIO(file_content))
            
            # Get class to check total students
            class_admin = user_crud.get_class_admin_by_id(db, id_class_admin)
            if not class_admin:
                raise NotFoundException("Class not found")
            
            # Get existing students count
            existing_students = db.query(Student).filter(
                Student.id_class_admin == id_class_admin
            ).count()
            
            new_students = []
            duplicates = []
            
            for _, row in df.iterrows():
                code = str(row.get('code_student', '')).strip()
                name = str(row.get('name_student', '')).strip()
                email = str(row.get('email_student', '')).strip() if 'email_student' in row else None
                phone = str(row.get('phone_student', '')).strip() if 'phone_student' in row else None
                dob = row.get('dob_student', None) if 'dob_student' in row else None
                
                if not code or not name:
                    continue
                
                # Check if student already exists
                existing = user_crud.get_student_by_code(db, code)
                if existing:
                    duplicates.append(code)
                    continue
                
                student = user_crud.create_student(
                    db,
                    code_student=code,
                    name_student=name,
                    email_student=email if email else None,
                    phone_student=phone if phone else None,
                    dob_student=dob if dob else None,
                    id_class_admin=id_class_admin
                )
                new_students.append(student)
            
            # Check if total exceeds class capacity
            total_after = existing_students + len(new_students)
            
            return {
                "success": True,
                "imported": len(new_students),
                "duplicates": duplicates,
                "total_students": total_after,
                "message": f"Imported {len(new_students)} students"
            }
        except Exception as e:
            raise Exception(f"Error importing students: {str(e)}")
    
    @staticmethod
    def get_student_statistics(db: Session):
        """Get student statistics by course"""
        courses = user_crud.get_all_courses(db)
        stats = []
        
        for course in courses:
            faculties = db.query(user_crud.Faculty).filter(
                user_crud.Faculty.id_course == course.id_course
            ).all()
            
            students_count = db.query(Student).join(
                user_crud.ClassAdmin,
                Student.id_class_admin == user_crud.ClassAdmin.id_class_admin
            ).filter(
                user_crud.ClassAdmin.id_course == course.id_course
            ).count()
            
            stats.append({
                "course_id": course.id_course,
                "course_name": course.name_course,
                "start_year": course.start_year_course,
                "end_year": course.end_year_course,
                "faculties_count": len(faculties),
                "students_count": students_count
            })
        
        return stats
    
    @staticmethod
    def get_students_by_filters(
        db: Session,
        id_course: int = None,
        id_faculty: int = None,
        id_class_admin: int = None
    ):
        """Get students with filters"""
        query = db.query(Student)
        
        if id_class_admin:
            query = query.filter(Student.id_class_admin == id_class_admin)
        elif id_course and id_faculty:
            query = query.join(
                user_crud.ClassAdmin,
                Student.id_class_admin == user_crud.ClassAdmin.id_class_admin
            ).filter(
                user_crud.ClassAdmin.id_course == id_course,
                user_crud.ClassAdmin.id_faculty == id_faculty
            )
        
        return query.all()