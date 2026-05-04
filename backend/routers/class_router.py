from fastapi import APIRouter, Depends, File, UploadFile, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from services.class_service import ClassService
from core.dependencies import get_current_teacher, get_current_admin
from models.auth_models import Login
from crud import auth_crud
from typing import List

router = APIRouter(prefix="/api/classes", tags=["classes"])

@router.get("/my-classes")
async def get_my_classes(
    current_user: Login = Depends(get_current_teacher),
    id_course: int = None,
    id_faculty: int = None,
    status: str = None,
    db: Session = Depends(get_db)
):
    """Get teacher's classes"""
    account = auth_crud.get_account_by_login_id(db, current_user.id_login)
    return ClassService.get_classes_by_teacher(
        db, account.id_account, id_course, id_faculty, status
    )

@router.get("/{class_id}")
async def get_class_info(
    class_id: int,
    current_user: Login = Depends(get_current_teacher),
    db: Session = Depends(get_db)
):
    """Get class information"""
    return ClassService.get_class_info(db, class_id)

@router.post("/admin/import")
async def import_classes(
    current_user: Login = Depends(get_current_admin),
    id_course: int = None,              # ✅ Thêm default
    id_faculty: int = None,             # ✅ Thêm default
    id_account_teacher: int = None,     # ✅ Thêm default
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """Import classes from Excel"""
    content = await file.read()
    return ClassService.import_classes_from_excel(
        db, id_course, id_faculty, id_account_teacher, content
    )

@router.post("/{class_id}/add-students")
async def add_students_to_class(
    class_id: int,
    student_codes: List[str],
    current_user: Login = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Add students to class"""
    return ClassService.add_students_to_class(db, class_id, student_codes)

@router.delete("/{class_id}/remove-student/{student_id}")
async def remove_student_from_class(
    class_id: int,
    student_id: int,
    current_user: Login = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Remove student from class"""
    from crud import class_crud
    success = class_crud.remove_student_from_class(db, student_id, class_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not in this class"
        )
    return {"message": "Student removed from class"}