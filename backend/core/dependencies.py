from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from core.security import verify_token
from models.auth_models import Login, Level
from models.user_models import Account

security = HTTPBearer()

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> Login:
    """Get current user from JWT token"""
    token = credentials.credentials
    try:
        payload = verify_token(token)
        login_id: int = payload.get("sub")
        if login_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )
    
    user = db.query(Login).filter(Login.id_login == login_id).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )
    
    if user.status_login != "ON":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is not active"
        )
    
    return user

async def get_current_teacher(
    current_user: Login = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Login:
    """Get current teacher user"""
    level = db.query(Level).filter(Level.id_level == current_user.id_level).first()
    if level.name_level != "teacher":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied. Teacher role required."
        )
    return current_user

async def get_current_admin(
    current_user: Login = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Login:
    """Get current admin user"""
    level = db.query(Level).filter(Level.id_level == current_user.id_level).first()
    if level.name_level != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied. Admin role required."
        )
    return current_user