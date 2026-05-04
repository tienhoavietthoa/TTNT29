from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from services.auth_service import AuthService
from schemas.auth_schemas import (
    LoginRegister, LoginRequest, TokenResponse, RefreshTokenRequest,
    ChangePasswordRequest, UserMeResponse
)
from core.dependencies import get_current_user
from models.auth_models import Login
from crud import auth_crud

router = APIRouter(prefix="/api/auth", tags=["auth"])

@router.post("/register", response_model=dict)
async def register_teacher(
    data: LoginRegister,
    db: Session = Depends(get_db)
):
    """Register teacher account"""
    return AuthService.register_teacher(
        db,
        code_login=data.code_login,
        name_account=data.name_account,
        email_account=data.email_account,
        password=data.password,
        confirm_password=data.confirm_password,
        phone_account=data.phone_account
    )

@router.post("/login", response_model=TokenResponse)
async def login(
    credentials: LoginRequest,
    db: Session = Depends(get_db)
):
    """Login user"""
    return AuthService.login(
        db,
        code_login=credentials.code_login,
        password=credentials.password
    )

@router.post("/refresh-token", response_model=TokenResponse)
async def refresh_token(
    data: RefreshTokenRequest,
    db: Session = Depends(get_db)
):
    """Refresh access token"""
    return AuthService.refresh_access_token(data.refresh_token)

@router.post("/change-password")
async def change_password(
    data: ChangePasswordRequest,
    current_user: Login = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Change password"""
    return AuthService.change_password(
        db,
        id_login=current_user.id_login,
        old_password=data.old_password,
        new_password=data.new_password,
        confirm_password=data.confirm_password
    )

@router.get("/me", response_model=UserMeResponse)
async def get_current_user_info(
    current_user: Login = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get current user information"""
    account = auth_crud.get_account_by_login_id(db, current_user.id_login)
    if not account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Account not found"
        )
    
    return {
        "id_account": account.id_account,
        "name_account": account.name_account,
        "email_account": account.email_account,
        "phone_account": account.phone_account,
        "login": current_user
    }