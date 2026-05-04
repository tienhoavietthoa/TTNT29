import requests
import json
from typing import Optional, Dict, Any
from config import config
from core.auth_manager import auth_manager

class APIClient:
    """HTTP client for API requests"""
    
    def __init__(self):
        self.base_url = config.API_BASE_URL
        self.timeout = 10
    
    def _get_headers(self, include_auth: bool = True) -> Dict[str, str]:
        """Get request headers"""
        headers = {
            "Content-Type": "application/json",
        }
        
        if include_auth and auth_manager.access_token:
            headers.update(auth_manager.get_auth_header())
        
        return headers
    
    def _handle_response(self, response: requests.Response) -> Dict[str, Any]:
        """Handle API response"""
        try:
            data = response.json()
        except:
            data = {"raw_response": response.text}
        
        return {
            "status_code": response.status_code,
            "success": response.status_code < 400,
            "data": data,
            "error": None if response.status_code < 400 else data.get("detail", "Unknown error")
        }
    
    def post(self, endpoint: str, data: Dict = None, include_auth: bool = True, files: Dict = None) -> Dict[str, Any]:
        """POST request"""
        try:
            url = f"{self.base_url}{endpoint}"
            headers = self._get_headers(include_auth)
            
            if files:
                # Remove Content-Type for multipart/form-data
                del headers["Content-Type"]
                response = requests.post(url, data=data, files=files, headers=headers, timeout=self.timeout)
            else:
                response = requests.post(url, json=data, headers=headers, timeout=self.timeout)
            
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            return {
                "status_code": 0,
                "success": False,
                "data": None,
                "error": f"Network error: {str(e)}"
            }
    
    def get(self, endpoint: str, params: Dict = None, include_auth: bool = True) -> Dict[str, Any]:
        """GET request"""
        try:
            url = f"{self.base_url}{endpoint}"
            headers = self._get_headers(include_auth)
            response = requests.get(url, params=params, headers=headers, timeout=self.timeout)
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            return {
                "status_code": 0,
                "success": False,
                "data": None,
                "error": f"Network error: {str(e)}"
            }
    
    def put(self, endpoint: str, data: Dict = None, include_auth: bool = True) -> Dict[str, Any]:
        """PUT request"""
        try:
            url = f"{self.base_url}{endpoint}"
            headers = self._get_headers(include_auth)
            response = requests.put(url, json=data, headers=headers, timeout=self.timeout)
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            return {
                "status_code": 0,
                "success": False,
                "data": None,
                "error": f"Network error: {str(e)}"
            }
    
    def delete(self, endpoint: str, include_auth: bool = True) -> Dict[str, Any]:
        """DELETE request"""
        try:
            url = f"{self.base_url}{endpoint}"
            headers = self._get_headers(include_auth)
            response = requests.delete(url, headers=headers, timeout=self.timeout)
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            return {
                "status_code": 0,
                "success": False,
                "data": None,
                "error": f"Network error: {str(e)}"
            }

api_client = APIClient()