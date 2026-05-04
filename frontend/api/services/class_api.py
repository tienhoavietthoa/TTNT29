from api.client import api_client
from typing import Dict, Tuple, Optional, List

class ClassAPI:
    """Class API calls"""
    
    @staticmethod
    def get_my_classes(id_course: int = None, id_faculty: int = None, status: str = None) -> Tuple[bool, Optional[List]]:
        """Get teacher's classes"""
        params = {}
        if id_course:
            params["id_course"] = id_course
        if id_faculty:
            params["id_faculty"] = id_faculty
        if status:
            params["status"] = status
        
        response = api_client.get("/classes/my-classes", params=params)
        
        if response["success"]:
            return True, response["data"]
        else:
            return False, None
    
    @staticmethod
    def get_class_info(class_id: int) -> Tuple[bool, Optional[Dict]]:
        """Get class information"""
        response = api_client.get(f"/classes/{class_id}")
        
        if response["success"]:
            return True, response["data"]
        else:
            return False, None
    
    @staticmethod
    def import_classes(id_course: int, id_faculty: int, id_account_teacher: int, file_path: str) -> Tuple[bool, str]:
        """Import classes from Excel (admin only)"""
        try:
            with open(file_path, 'rb') as f:
                files = {'file': f}
                data = {
                    'id_course': id_course,
                    'id_faculty': id_faculty,
                    'id_account_teacher': id_account_teacher
                }
                response = api_client.post(
                    "/classes/admin/import",
                    data=data,
                    files=files
                )
            
            if response["success"]:
                result = response["data"]
                return True, f"Imported: {result.get('imported', 0)} classes"
            else:
                return False, response["error"]
        except Exception as e:
            return False, f"Error: {str(e)}"
    
    @staticmethod
    def add_students_to_class(class_id: int, student_codes: List[str]) -> Tuple[bool, str]:
        """Add students to class (admin only)"""
        data = {"student_codes": student_codes}
        response = api_client.post(f"/classes/{class_id}/add-students", data=data)
        
        if response["success"]:
            result = response["data"]
            msg = f"Added: {len(result.get('added', []))} students"
            return True, msg
        else:
            return False, response["error"]
    
    @staticmethod
    def remove_student_from_class(class_id: int, student_id: int) -> Tuple[bool, str]:
        """Remove student from class (admin only)"""
        response = api_client.delete(f"/classes/{class_id}/remove-student/{student_id}")
        
        if response["success"]:
            return True, "Removed student from class"
        else:
            return False, response["error"]