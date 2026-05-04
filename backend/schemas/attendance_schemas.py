from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class AttendanceCreate(BaseModel):
    id_student: int
    status_attendance: str  # present, absent, manual
    notes_attendance: Optional[str] = None

class AttendanceManualCreate(BaseModel):
    id_student: int
    notes_attendance: str

class AttendanceResponse(BaseModel):
    id_attendance: int
    id_student: int
    status_attendance: str
    checkin_time_attendance: Optional[datetime]
    img_filename_attendance: Optional[str]
    notes_attendance: Optional[str]
    created_at_attendance: datetime
    
    class Config:
        from_attributes = True