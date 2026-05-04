from api.client import api_client
from typing import Dict, Tuple, Optional, List

class MessageAPI:
    """Message API calls"""
    
    @staticmethod
    def send_message(receiver_id_login: int, content_message: str) -> Tuple[bool, str]:
        """Send message"""
        data = {
            "receiver_id_login": receiver_id_login,
            "content_message": content_message
        }
        
        response = api_client.post("/messages/send", data=data)
        
        if response["success"]:
            return True, "Gửi tin nhắn thành công"
        else:
            return False, response["error"]
    
    @staticmethod
    def get_conversation(user_id: int) -> Tuple[bool, Optional[List]]:
        """Get conversation with another user"""
        response = api_client.get(f"/messages/conversation/{user_id}")
        
        if response["success"]:
            return True, response["data"]
        else:
            return False, None
    
    @staticmethod
    def get_my_conversations() -> Tuple[bool, Optional[Dict]]:
        """Get all my conversations"""
        response = api_client.get("/messages/")
        
        if response["success"]:
            return True, response["data"]
        else:
            return False, None