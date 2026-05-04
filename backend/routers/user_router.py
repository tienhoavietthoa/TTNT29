from fastapi import APIRouter, Depends, File, UploadFile, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from services.user_service import UserService
from core.dependencies import get_current_teacher, get_current_admin
from models.auth_models import Login
from schemas.user_schemas import StudentResponse
from typing import List

router = APIRouter(prefix="/api/users", tags=["users"])

@router.get("/me/profile")
async def get_my_profile(
    current_user: Login = Depends(get_current_teacher),
    db: Session = Depends(get_db)
):
    """Get current teacher's profile"""
    from crud import auth_crud
    account = auth_crud.get_account_by_login_id(db, current_user.id_login)
    return {
        "name": account.name_account,
        "email": account.email_account,
        "phone": account.phone_account
    }

@router.get("/admin/students/statistics")
async def get_student_statistics(
    current_user: Login = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Get student statistics by course"""
    return UserService.get_student_statistics(db)

@router.get("/admin/students")
async def get_students_by_filters(
    current_user: Login = Depends(get_current_admin),
    id_course: int = None,
    id_faculty: int = None,
    id_class_admin: int = None,
    db: Session = Depends(get_db)
):
    """Get students with filters"""
    students = UserService.get_students_by_filters(
        db, id_course, id_faculty, id_class_admin
    )
    return students

@router.post("/admin/students/import")
async def import_students(
    current_user: Login = Depends(get_current_admin),
    id_course: int = None,           # ✅ Thêm default
    id_faculty: int = None,          # ✅ Thêm default
    id_class_admin: int = None,      # ✅ Thêm default
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """Import students from Excel"""
    content = await file.read()
    return UserService.import_students_from_excel(
        db, id_course, id_faculty, id_class_admin, content
    )


@router.delete("/admin/students/{student_id}")
async def delete_student(
    student_id: int,
    current_user: Login = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Delete student"""
    from crud import user_crud
    success = user_crud.delete_student(db, student_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )
    return {"message": "Student deleted successfully"}