from sqlalchemy.orm import Session
from sqlalchemy import and_
from models.user_models import Student, Course, Faculty, ClassAdmin
from datetime import date

def create_student(
    db: Session,
    code_student: str,
    name_student: str,
    email_student: str = None,
    phone_student: str = None,
    dob_student: date = None,
    id_class_admin: int = None
) -> Student:
    """Create student"""
    db_student = Student(
        code_student=code_student,
        name_student=name_student,
        email_student=email_student,
        phone_student=phone_student,
        dob_student=dob_student,
        id_class_admin=id_class_admin
    )
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student

def get_student_by_id(db: Session, id_student: int) -> Student:
    """Get student by id"""
    return db.query(Student).filter(Student.id_student == id_student).first()

def get_student_by_code(db: Session, code_student: str) -> Student:
    """Get student by code"""
    return db.query(Student).filter(Student.code_student == code_student).first()

def get_students_by_class(db: Session, id_class_admin: int):
    """Get all students in class"""
    return db.query(Student).filter(Student.id_class_admin == id_class_admin).all()

def get_students_by_course_and_faculty(
    db: Session,
    id_course: int = None,
    id_faculty: int = None
):
    """Get students by course and faculty"""
    query = db.query(Student)
    
    if id_course and id_faculty:
        query = query.join(ClassAdmin).filter(
            and_(
                ClassAdmin.id_course == id_course,
                ClassAdmin.id_faculty == id_faculty
            )
        )
    
    return query.all()

def delete_student(db: Session, id_student: int) -> bool:
    """Delete student"""
    db_student = get_student_by_id(db, id_student)
    if not db_student:
        return False
    db.delete(db_student)
    db.commit()
    return True

def get_course_by_id(db: Session, id_course: int) -> Course:
    """Get course by id"""
    return db.query(Course).filter(Course.id_course == id_course).first()

def get_all_courses(db: Session):
    """Get all courses"""
    return db.query(Course).all()

def get_faculty_by_id(db: Session, id_faculty: int) -> Faculty:
    """Get faculty by id"""
    return db.query(Faculty).filter(Faculty.id_faculty == id_faculty).first()

def get_all_faculties(db: Session):
    """Get all faculties"""
    return db.query(Faculty).all()

def get_class_admin_by_id(db: Session, id_class_admin: int) -> ClassAdmin:
    """Get class admin by id"""
    return db.query(ClassAdmin).filter(ClassAdmin.id_class_admin == id_class_admin).first()

def get_class_admins_by_course_and_faculty(
    db: Session,
    id_course: int,
    id_faculty: int
):
    """Get class admins by course and faculty"""
    return db.query(ClassAdmin).filter(
        and_(
            ClassAdmin.id_course == id_course,
            ClassAdmin.id_faculty == id_faculty
        )
    ).all()