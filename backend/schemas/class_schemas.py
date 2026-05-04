from pydantic import BaseModel
from datetime import date, time, datetime
from typing import Optional, List

class SessionAttendanceResponse(BaseModel):
    id_session_attendance: int
    session_number: int
    session_date: date
    session_start_hour: Optional[time]
    session_end_hour: Optional[time]
    status_session: Optional[str]
    
    class Config:
        from_attributes = True

class ClassAttendanceCreate(BaseModel):
    code_class_attendance: str
    name_class_attendance: str
    id_faculty: int
    id_course: int
    id_account_teacher: int
    total_students_class_attendance: int
    lesson_day_class_attendance: str
    lesson_start_hour: time
    lesson_end_hour: time
    start_date_class_attendance: date
    end_date_class_attendance: date

class ClassAttendanceResponse(BaseModel):
    id_class_attendance: int
    code_class_attendance: str
    name_class_attendance: str
    status_class_attendance: str
    total_students_class_attendance: int
    lesson_day_class_attendance: str
    lesson_start_hour: Optional[time]
    lesson_end_hour: Optional[time]
    start_date_class_attendance: date
    end_date_class_attendance: date
    
    class Config:
        from_attributes = True

class StudentClassAttendanceResponse(BaseModel):
    id_student: int
    code_student: str
    name_student: str
    email_student: Optional[str]
    
    class Config:
        from_attributes = True