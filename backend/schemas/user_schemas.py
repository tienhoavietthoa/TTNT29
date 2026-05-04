from pydantic import BaseModel, EmailStr
from datetime import date, datetime
from typing import Optional

class CourseResponse(BaseModel):
    id_course: int
    start_year_course: int
    end_year_course: int
    name_course: str
    
    class Config:
        from_attributes = True

class FacultyResponse(BaseModel):
    id_faculty: int
    fullname_faculty: str
    shortname_faculty: str
    
    class Config:
        from_attributes = True

class ClassAdminResponse(BaseModel):
    id_class_admin: int
    name_class_admin: str
    id_faculty: int
    id_course: int
    
    class Config:
        from_attributes = True

class AccountResponse(BaseModel):
    id_account: int
    name_account: str
    email_account: str
    phone_account: Optional[str]
    
    class Config:
        from_attributes = True

class StudentCreate(BaseModel):
    code_student: str
    name_student: str
    email_student: Optional[str]
    phone_student: Optional[str]
    dob_student: Optional[date]
    id_class_admin: int

class StudentResponse(BaseModel):
    id_student: int
    code_student: str
    name_student: str
    email_student: Optional[str]
    phone_student: Optional[str]
    dob_student: Optional[date]
    status_student: str
    created_at_student: datetime
    
    class Config:
        from_attributes = True