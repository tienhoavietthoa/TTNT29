from typing import Optional
from PyQt5.QtWidgets import QStackedWidget, QMainWindow

class AppManager:
    """Manage application state and window transitions"""
    
    def __init__(self):
        self.stacked_widget: Optional[QStackedWidget] = None
        self.current_window = None
        self.user_data = None
        self.user_role = None  # 'teacher', 'admin', 'student'
    
    def set_stacked_widget(self, widget: QStackedWidget):
        """Set the main stacked widget"""
        self.stacked_widget = widget
    
    def switch_to_window(self, window_name: str):
        """Switch to a specific window"""
        if self.stacked_widget:
            index = self.stacked_widget.findChild(type(None), window_name)
            if index >= 0:
                self.stacked_widget.setCurrentIndex(index)
    
    def set_user_data(self, user_data: dict, role: str):
        """Set current user data"""
        self.user_data = user_data
        self.user_role = role
    
    def get_user_role(self) -> Optional[str]:
        """Get current user role"""
        return self.user_role
    
    def clear_user_data(self):
        """Clear user data on logout"""
        self.user_data = None
        self.user_role = None

app_manager = AppManager()