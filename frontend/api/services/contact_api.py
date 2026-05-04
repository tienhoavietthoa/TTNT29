from api.client import api_client
from typing import Tuple

class ContactAPI:
    """Contact API calls"""
    
    @staticmethod
    def submit_contact(
        sender_name: str,
        user_type: str,
        email: str,
        phone: str,
        content: str
    ) -> Tuple[bool, str]:
        """Submit contact form (public)"""
        data = {
            "sender_name_contact": sender_name,
            "user_type_contact": user_type,
            "email_contact": email,
            "phone_contact": phone,
            "content_contact": content
        }
        
        response = api_client.post("/contacts/", data=data, include_auth=False)
        
        if response["success"]:
            return True, "Liên hệ đã được gửi thành công"
        else:
            return False, response["error"]
    
    @staticmethod
    def get_all_contacts():
        """Get all contacts (admin only)"""
        response = api_client.get("/contacts/admin/all")
        
        if response["success"]:
            return True, response["data"]
        else:
            return False, None