from api.client import api_client
from core.auth_manager import auth_manager
from typing import Dict, Tuple, Optional

class AuthAPI:
    """Authentication API calls"""
    
    @staticmethod
    def register_teacher(
        code_login: str,
        name_account: str,
        email_account: str,
        password: str,
        confirm_password: str,
        phone_account: str = None
    ) -> Tuple[bool, str]:
        """Register teacher account"""
        data = {
            "code_login": code_login,
            "name_account": name_account,
            "email_account": email_account,
            "password": password,
            "confirm_password": confirm_password,
            "phone_account": phone_account
        }
        
        response = api_client.post("/auth/register", data=data, include_auth=False)
        
        if response["success"]:
            return True, "Đăng ký thành công. Vui lòng chờ duyệt từ admin."
        else:
            return False, response["error"]
    
    @staticmethod
    def login(code_login: str, password: str) -> Tuple[bool, str]:
        """Login user"""
        data = {
            "code_login": code_login,
            "password": password
        }
        
        response = api_client.post("/auth/login", data=data, include_auth=False)
        
        if response["success"]:
            token_data = response["data"]
            auth_manager.save_tokens(
                token_data["access_token"],
                token_data["refresh_token"],
                token_data["login_id"]
            )
            return True, "Đăng nhập thành công"
        else:
            return False, response["error"]
    
    @staticmethod
    def get_current_user() -> Tuple[bool, Optional[Dict]]:
        """Get current user info"""
        response = api_client.get("/auth/me")
        
        if response["success"]:
            return True, response["data"]
        else:
            return False, None
    
    @staticmethod
    def change_password(old_password: str, new_password: str, confirm_password: str) -> Tuple[bool, str]:
        """Change password"""
        data = {
            "old_password": old_password,
            "new_password": new_password,
            "confirm_password": confirm_password
        }
        
        response = api_client.post("/auth/change-password", data=data)
        
        if response["success"]:
            return True, "Mật khẩu đã được thay đổi thành công"
        else:
            return False, response["error"]
    
    @staticmethod
    def logout():
        """Logout user"""
        auth_manager.clear_tokens()