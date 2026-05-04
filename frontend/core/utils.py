import os
import cv2
import numpy as np
from PIL import Image
from datetime import datetime
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import QMessageBox
from config import config

class ImageUtils:
    """Utility functions for image handling"""
    
    @staticmethod
    def create_upload_dir():
        """Create upload directory if not exists"""
        if not os.path.exists(config.UPLOAD_DIR):
            os.makedirs(config.UPLOAD_DIR)
        if not os.path.exists(config.TEMP_IMAGE_DIR):
            os.makedirs(config.TEMP_IMAGE_DIR)
    
    @staticmethod
    def save_image(image_path: str, student_id: int, class_id: int) -> str:
        """Save image to upload directory"""
        ImageUtils.create_upload_dir()
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"student_{student_id}_class_{class_id}_{timestamp}.jpg"
        filepath = os.path.join(config.UPLOAD_DIR, filename)
        
        img = cv2.imread(image_path)
        cv2.imwrite(filepath, img)
        return filename
    
    @staticmethod
    def load_image_as_qpixmap(image_path: str, width: int = 200, height: int = 200) -> QPixmap:
        """Load image and return as QPixmap"""
        try:
            img = Image.open(image_path)
            img.thumbnail((width, height), Image.Resampling.LANCZOS)
            
            # Convert to RGB if necessary
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            # Convert to QPixmap
            data = img.tobytes('raw', 'RGB')
            qimg = QImage(data, img.width, img.height, QImage.Format_RGB888)
            return QPixmap.fromImage(qimg)
        except Exception as e:
            print(f"Error loading image: {e}")
            return QPixmap()
    
    @staticmethod
    def convert_cv_image_to_qpixmap(cv_image, width: int = 200, height: int = 200) -> QPixmap:
        """Convert OpenCV image to QPixmap"""
        try:
            rgb_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)
            h, w, ch = rgb_image.shape
            bytes_per_line = ch * w
            qt_image = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(qt_image)
            
            # Scale to desired size
            return pixmap.scaledToWidth(width)
        except Exception as e:
            print(f"Error converting image: {e}")
            return QPixmap()
    
    @staticmethod
    def delete_image(filename: str) -> bool:
        """Delete image file"""
        try:
            filepath = os.path.join(config.UPLOAD_DIR, filename)
            if os.path.exists(filepath):
                os.remove(filepath)
                return True
        except Exception as e:
            print(f"Error deleting image: {e}")
        return False

class DialogUtils:
    """Utility functions for dialogs"""
    
    @staticmethod
    def show_info(parent, title: str, message: str):
        """Show info message box"""
        QMessageBox.information(parent, title, message)
    
    @staticmethod
    def show_warning(parent, title: str, message: str):
        """Show warning message box"""
        QMessageBox.warning(parent, title, message)
    
    @staticmethod
    def show_error(parent, title: str, message: str):
        """Show error message box"""
        QMessageBox.critical(parent, title, message)
    
    @staticmethod
    def ask_question(parent, title: str, message: str) -> bool:
        """Show question message box"""
        reply = QMessageBox.question(parent, title, message,
                                     QMessageBox.Yes | QMessageBox.No)
        return reply == QMessageBox.Yes
    
    @staticmethod
    def ask_yesnocancel(parent, title: str, message: str):
        """Show yes/no/cancel message box"""
        reply = QMessageBox.question(parent, title, message,
                                     QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
        return reply

class DateTimeUtils:
    """Utility functions for date and time"""
    
    @staticmethod
    def get_current_datetime_string() -> str:
        """Get current datetime as string"""
        return datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    
    @staticmethod
    def get_current_date_string() -> str:
        """Get current date as string"""
        return datetime.now().strftime("%d/%m/%Y")
    
    @staticmethod
    def get_current_time_string() -> str:
        """Get current time as string"""
        return datetime.now().strftime("%H:%M:%S")
    
    @staticmethod
    def format_datetime(dt_str: str) -> str:
        """Format datetime string"""
        try:
            dt = datetime.fromisoformat(dt_str.replace('Z', '+00:00'))
            return dt.strftime("%d/%m/%Y %H:%M:%S")
        except:
            return dt_str

class ValidationUtils:
    """Utility functions for validation"""
    
    @staticmethod
    def validate_email(email: str) -> bool:
        """Validate email format"""
        import re
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    @staticmethod
    def validate_phone(phone: str) -> bool:
        """Validate phone number"""
        import re
        pattern = r'^[0-9]{10,}$'
        return re.match(pattern, phone.replace('-', '').replace(' ', '')) is not None
    
    @staticmethod
    def validate_password(password: str) -> tuple:
        """Validate password strength"""
        errors = []
        if len(password) < 6:
            errors.append("Mật khẩu phải có ít nhất 6 ký tự")
        if not any(c.isupper() for c in password):
            errors.append("Mật khẩu phải chứa ít nhất một chữ cái viết hoa")
        if not any(c.isdigit() for c in password):
            errors.append("Mật khẩu phải chứa ít nhất một chữ số")
        
        return len(errors) == 0, errors