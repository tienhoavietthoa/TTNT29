from fastapi import APIRouter, Depends, File, UploadFile, HTTPException, status
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.services.face_recognition_service import FaceRecognitionService
from backend.core.dependencies import get_current_teacher, get_current_admin
from backend.models.auth_models import Login
from pydantic import BaseModel

router = APIRouter(prefix="/api/face", tags=["face"])

class EnrollRequest(BaseModel):
    id_student: int
    id_class_attendance: int

@router.post("/enroll")
async def enroll_face(
    id_student: int,
    id_class_attendance: int,
    file: UploadFile = File(...),
    current_user: Login = Depends(get_current_teacher),
    db: Session = Depends(get_db)
):
    """Enroll student face"""
    try:
        image_data = await file.read()
        result = FaceRecognitionService.process_enrollment_image(
            image_data, id_student, id_class_attendance
        )
        
        if not result['success']:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=result['error']
            )
        
        return result
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.post("/check-attendance")
async def check_attendance(
    id_class_attendance: int,
    id_session_attendance: int,
    file: UploadFile = File(...),
    current_user: Login = Depends(get_current_teacher),
    db: Session = Depends(get_db)
):
    """Check attendance with face"""
    try:
        image_data = await file.read()
        result = FaceRecognitionService.process_attendance_image(
            image_data, id_class_attendance, id_session_attendance, db
        )
        
        if not result['success']:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=result['error']
            )
        
        return result
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.get("/check-similar/{class_id}")
async def check_similar_faces(
    class_id: int,
    current_user: Login = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Check for duplicate faces in class"""
    # Implementation for quality control
    return {"message": "Checking similar faces"}