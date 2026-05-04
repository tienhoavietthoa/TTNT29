from api.client import api_client
from typing import Dict, Tuple, Optional, List

class AttendanceAPI:
    """Attendance API calls"""
    
    @staticmethod
    def get_session_details(session_id: int) -> Tuple[bool, Optional[Dict]]:
        """Get session attendance details"""
        response = api_client.get(f"/attendance/session/{session_id}")
        
        if response["success"]:
            return True, response["data"]
        else:
            return False, None
    
    @staticmethod
    def checkin_student(session_id: int, class_id: int, student_id: int, img_filename: str = None) -> Tuple[bool, str]:
        """Check in student"""
        data = {
            "id_student": student_id,
            "img_filename": img_filename
        }
        
        response = api_client.post(f"/attendance/checkin/{session_id}/{class_id}", data=data)
        
        if response["success"]:
            return True, "Điểm danh thành công"
        else:
            return False, response["error"]
    
    @staticmethod
    def manual_checkin_student(session_id: int, class_id: int, student_id: int, notes: str) -> Tuple[bool, str]:
        """Manual check in student"""
        data = {
            "id_student": student_id,
            "notes": notes
        }
        
        response = api_client.post(f"/attendance/manual-checkin/{session_id}/{class_id}", data=data)
        
        if response["success"]:
            return True, "Điểm danh thủ công thành công"
        else:
            return False, response["error"]
    
    @staticmethod
    def get_student_attendance_in_class(student_id: int, class_id: int) -> Tuple[bool, Optional[Dict]]:
        """Get student attendance in class"""
        response = api_client.get(f"/attendance/student/{student_id}/class/{class_id}")
        
        if response["success"]:
            return True, response["data"]
        else:
            return False, None
    
    @staticmethod
    def search_student_attendance(code_student: str, code_class: str) -> Tuple[bool, Optional[List]]:
        """Search student attendance (public)"""
        params = {
            "code_student": code_student,
            "code_class": code_class
        }
        
        response = api_client.get("/attendance/public/search", params=params, include_auth=False)
        
        if response["success"]:
            return True, response["data"]
        else:
            return False, None