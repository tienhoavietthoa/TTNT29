from sqlalchemy.orm import Session
from crud import auth_crud, user_crud
from core.security import create_access_token, create_refresh_token, verify_token
from core.exceptions import (
    InvalidCredentialsException,
    ConflictException,
    BadRequestException
)
from datetime import timedelta
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config import get_settings

settings = get_settings()

class AuthService:
    @staticmethod
    def register_teacher(
        db: Session,
        code_login: str,
        name_account: str,
        email_account: str,
        password: str,
        confirm_password: str,
        phone_account: str = None
    ):
        """Register teacher account"""
        # Validate password
        if password != confirm_password:
            raise BadRequestException("Passwords do not match")
        
        # Check if code already exists
        existing_login = auth_crud.get_login_by_code(db, code_login)
        if existing_login:
            raise ConflictException("Code already exists")
        
        # Check if email already exists
        existing_email = db.query(user_crud.Account).filter(
            user_crud.Account.email_account == email_account
        ).first()
        if existing_email:
            raise ConflictException("Email already exists")
        
        # Get teacher level
        levels = auth_crud.get_all_levels(db)
        teacher_level = next((l for l in levels if l.name_level == "teacher"), None)
        
        if not teacher_level:
            raise BadRequestException("Teacher level not found")
        
        # Create login
        db_login = auth_crud.create_login(
            db,
            code_login=code_login,
            password=password,
            id_level=teacher_level.id_level,
            status_login="OFF"  # Wait for approval
        )
        
        # Create account
        db_account = auth_crud.create_account(
            db,
            name_account=name_account,
            email_account=email_account,
            phone_account=phone_account,
            id_login=db_login.id_login
        )
        
        # Send email
        AuthService.send_approval_pending_email(email_account, name_account)
        
        return {
            "message": "Registration successful. Awaiting admin approval.",
            "login_id": db_login.id_login
        }
    
    @staticmethod
    def login(db: Session, code_login: str, password: str):
        """Login user"""
        user = auth_crud.authenticate_login(db, code_login, password)
        
        if not user:
            raise InvalidCredentialsException()
        
        if user.status_login != "ON":
            raise BadRequestException(
                f"Account status: {user.status_login}. "
                "Awaiting admin approval or account is locked."
            )
        
        # Create tokens
        access_token = create_access_token(
            data={"sub": user.id_login}
        )
        refresh_token = create_refresh_token(
            data={"sub": user.id_login}
        )
        
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "login_id": user.id_login
        }
    
    @staticmethod
    def refresh_access_token(refresh_token: str):
        """Refresh access token"""
        payload = verify_token(refresh_token)
        login_id = payload.get("sub")
        
        if not login_id:
            raise InvalidCredentialsException()
        
        new_access_token = create_access_token(
            data={"sub": login_id}
        )
        
        return {
            "access_token": new_access_token,
            "token_type": "bearer"
        }
    
    @staticmethod
    def change_password(
        db: Session,
        id_login: int,
        old_password: str,
        new_password: str,
        confirm_password: str
    ):
        """Change password"""
        # Validate new passwords match
        if new_password != confirm_password:
            raise BadRequestException("Passwords do not match")
        
        # Get user
        user = auth_crud.get_login_by_id(db, id_login)
        if not user:
            raise BadRequestException("User not found")
        
        # Verify old password
        from core.security import verify_password
        if not verify_password(old_password, user.pass_login):
            raise InvalidCredentialsException("Old password is incorrect")
        
        # Update password
        auth_crud.update_login_password(db, id_login, new_password)
        
        return {"message": "Password changed successfully"}
    
    @staticmethod
    def send_approval_pending_email(email: str, name: str):
        """Send approval pending email"""
        try:
            subject = "Tài khoản đang chờ duyệt - Hệ thống điểm danh"
            body = f"""
Xin chào {name},

Tài khoản của bạn đã được đăng ký thành công và hiện đang chờ duyệt từ admin.
Bạn sẽ nhận được email xác nhận khi tài khoản được duyệt.

Vui lòng chờ kết quả...

Best regards,
Hệ thống Điểm Danh Sinh Viên
            """
            AuthService._send_email(email, subject, body)
        except Exception as e:
            print(f"Error sending email: {str(e)}")
    
    @staticmethod
    def send_approval_email(email: str, name: str):
        """Send approval email"""
        try:
            subject = "Tài khoản được duyệt - Hệ thống điểm danh"
            body = f"""
Xin chào {name},

Chúc mừng! Tài khoản của bạn đã được duyệt và kích hoạt.
Bạn có thể đăng nhập vào hệ thống ngay bây giờ.

Best regards,
Hệ thống Điểm Danh Sinh Viên
            """
            AuthService._send_email(email, subject, body)
        except Exception as e:
            print(f"Error sending email: {str(e)}")
    
    @staticmethod
    def send_rejection_email(email: str, name: str):
        """Send rejection email"""
        try:
            subject = "Tài khoản bị từ chối - Hệ thống điểm danh"
            body = f"""
Xin chào {name},

Tài khoản của bạn đã bị từ chối. Vui lòng gửi lại thông tin hoặc liên hệ admin.

Best regards,
Hệ thống Điểm Danh Sinh Viên
            """
            AuthService._send_email(email, subject, body)
        except Exception as e:
            print(f"Error sending email: {str(e)}")
    
    @staticmethod
    def _send_email(to_email: str, subject: str, body: str):
        """Send email via SMTP"""
        try:
            msg = MIMEMultipart()
            msg['From'] = settings.SMTP_EMAIL
            msg['To'] = to_email
            msg['Subject'] = subject
            
            msg.attach(MIMEText(body, 'plain'))
            
            with smtplib.SMTP(settings.SMTP_SERVER, settings.SMTP_PORT) as server:
                server.starttls()
                server.login(settings.SMTP_EMAIL, settings.SMTP_PASSWORD)
                server.send_message(msg)
        except Exception as e:
            print(f"Error sending email: {str(e)}")