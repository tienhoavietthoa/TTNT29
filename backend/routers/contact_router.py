from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from services.contact_service import ContactService
from core.dependencies import get_current_admin
from models.auth_models import Login
from schemas.contact_schemas import ContactCreate

router = APIRouter(prefix="/api/contacts", tags=["contacts"])

@router.post("/")
async def create_contact(
    data: ContactCreate,
    db: Session = Depends(get_db)
):
    """Submit contact form (public endpoint)"""
    return ContactService.create_contact(
        db,
        sender_name_contact=data.sender_name_contact,
        user_type_contact=data.user_type_contact,
        email_contact=data.email_contact,
        phone_contact=data.phone_contact,
        content_contact=data.content_contact
    )

@router.get("/admin/all")
async def get_all_contacts(
    current_user: Login = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Get all contact submissions (admin only)"""
    return ContactService.get_all_contacts(db)