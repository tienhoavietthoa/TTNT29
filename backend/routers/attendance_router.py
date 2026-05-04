from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from services.attendance_service import AttendanceService
from core.dependencies import get_current_teacher
from models.auth_models import Login
from schemas.attendance_schemas import AttendanceCreate, AttendanceManualCreate
from pydantic import BaseModel

router = APIRouter(prefix="/api/attendance", tags=["attendance"])

class CheckinRequest(BaseModel):
    id_student: int
    img_filename: str = None
    id_embedding: int = None

class ManualCheckinRequest(BaseModel):
    id_student: int
    notes: str

@router.get("/session/{session_id}")
async def get_session_details(
    session_id: int,
    current_user: Login = Depends(get_current_teacher),
    db: Session = Depends(get_db)
):
    """Get session attendance details"""
    return AttendanceService.get_session_attendance_details(db, session_id)

@router.post("/checkin/{session_id}/{class_id}")
async def checkin_student(
    session_id: int,
    class_id: int,
    data: CheckinRequest,
    current_user: Login = Depends(get_current_teacher),
    db: Session = Depends(get_db)
):
    """Check in student"""
    return AttendanceService.checkin_student(
        db, session_id, data.id_student, class_id,
        data.img_filename, data.id_embedding
    )

@router.post("/manual-checkin/{session_id}/{class_id}")
async def manual_checkin_student(
    session_id: int,
    class_id: int,
    data: ManualCheckinRequest,
    current_user: Login = Depends(get_current_teacher),
    db: Session = Depends(get_db)
):
    """Manual check in student"""
    return AttendanceService.manual_checkin_student(
        db, session_id, data.id_student, class_id, data.notes
    )

@router.get("/student/{student_id}/class/{class_id}")
async def get_student_attendance_in_class(
    student_id: int,
    class_id: int,
    current_user: Login = Depends(get_current_teacher),
    db: Session = Depends(get_db)
):
    """Get student attendance records in class"""
    return AttendanceService.get_student_attendance_in_class(
        db, student_id, class_id
    )

# Public endpoint for students
@router.get("/public/search")
async def search_student_attendance(
    code_student: str,
    code_class: str,
    db: Session = Depends(get_db)
):
    """Search student attendance (no auth required)"""
    from crud import user_crud, class_crud, attendance_crud
    
    student = user_crud.get_student_by_code(db, code_student)
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )
    
    db_class = class_crud.get_class_attendance_by_code(db, code_class)
    if not db_class:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Class not found"
        )
    
    sessions = class_crud.get_sessions_by_class(db, db_class.id_class_attendance)
    
    sessions_data = []
    for session in sessions:
        attendance = attendance_crud.get_attendance_by_session_and_student(
            db, session.id_session_attendance, student.id_student
        )
        sessions_data.append({
            "session": session,
            "attendance": attendance
        })
    
    return sessions_data