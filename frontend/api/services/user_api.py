from api.client import api_client
from typing import Dict, Tuple, Optional, List

class UserAPI:
    """User API calls"""
    
    @staticmethod
    def get_my_profile() -> Tuple[bool, Optional[Dict]]:
        """Get current teacher's profile"""
        response = api_client.get("/users/me/profile")
        
        if response["success"]:
            return True, response["data"]
        else:
            return False, None
    
    @staticmethod
    def get_student_statistics() -> Tuple[bool, Optional[List]]:
        """Get student statistics by course (admin only)"""
        response = api_client.get("/users/admin/students/statistics")
        
        if response["success"]:
            return True, response["data"]
        else:
            return False, None
    
    @staticmethod
    def get_students(id_course: int = None, id_faculty: int = None, id_class_admin: int = None) -> Tuple[bool, Optional[List]]:
        """Get students with filters (admin only)"""
        params = {}
        if id_course:
            params["id_course"] = id_course
        if id_faculty:
            params["id_faculty"] = id_faculty
        if id_class_admin:
            params["id_class_admin"] = id_class_admin
        
        response = api_client.get("/users/admin/students", params=params)
        
        if response["success"]:
            return True, response["data"]
        else:
            return False, None
    
    @staticmethod
    def import_students(id_course: int, id_faculty: int, id_class_admin: int, file_path: str) -> Tuple[bool, str]:
        """Import students from Excel (admin only)"""
        try:
            with open(file_path, 'rb') as f:
                files = {'file': f}
                data = {
                    'id_course': id_course,
                    'id_faculty': id_faculty,
                    'id_class_admin': id_class_admin
                }
                response = api_client.post(
                    "/users/admin/students/import",
                    data=data,
                    files=files
                )
            
            if response["success"]:
                result = response["data"]
                msg = f"Imported: {result.get('imported', 0)}"
                return True, msg
            else:
                return False, response["error"]
        except Exception as e:
            return False, f"Error: {str(e)}"
    
    @staticmethod
    def delete_student(student_id: int) -> Tuple[bool, str]:
        """Delete student (admin only)"""
        response = api_client.delete(f"/users/admin/students/{student_id}")
        
        if response["success"]:
            return True, "Xóa sinh viên thành công"
        else:
            return False, response["error"]