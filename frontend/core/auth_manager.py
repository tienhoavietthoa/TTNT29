import json
import os
from typing import Optional, Dict
from config import config

class AuthManager:
    """Manage authentication and token storage"""
    
    def __init__(self):
        self.token_file = config.TOKEN_FILE
        self.current_user = None
        self.access_token = None
        self.refresh_token = None
        self.login_id = None
    
    def save_tokens(self, access_token: str, refresh_token: str, login_id: int):
        """Save tokens to file"""
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.login_id = login_id
        
        try:
            with open(self.token_file, 'w') as f:
                json.dump({
                    'access_token': access_token,
                    'refresh_token': refresh_token,
                    'login_id': login_id
                }, f)
        except Exception as e:
            print(f"Error saving tokens: {e}")
    
    def load_tokens(self) -> bool:
        """Load tokens from file"""
        try:
            if os.path.exists(self.token_file):
                with open(self.token_file, 'r') as f:
                    data = json.load(f)
                    self.access_token = data.get('access_token')
                    self.refresh_token = data.get('refresh_token')
                    self.login_id = data.get('login_id')
                    return True
        except Exception as e:
            print(f"Error loading tokens: {e}")
        return False
    
    def clear_tokens(self):
        """Clear stored tokens"""
        self.access_token = None
        self.refresh_token = None
        self.login_id = None
        self.current_user = None
        
        try:
            if os.path.exists(self.token_file):
                os.remove(self.token_file)
        except Exception as e:
            print(f"Error clearing tokens: {e}")
    
    def is_authenticated(self) -> bool:
        """Check if user is authenticated"""
        return self.access_token is not None
    
    def set_current_user(self, user_data: Dict):
        """Set current user info"""
        self.current_user = user_data
    
    def get_auth_header(self) -> Dict[str, str]:
        """Get authorization header"""
        if self.access_token:
            return {"Authorization": f"Bearer {self.access_token}"}
        return {}

auth_manager = AuthManager()