import sys
import os
from pathlib import Path

# ✅ Thêm dòng này
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PyQt5.QtWidgets import QApplication, QStackedWidget, QMainWindow, QWidget, QVBoxLayout
from PyQt5.QtCore import Qt

# ✅ SỬA: Loại bỏ "frontend." prefix
from ui.windows import LoginWindow, TeacherDashboardWindow
from ui.windows.admin_dashboard_window import AdminDashboardWindow
from core.auth_manager import auth_manager
from core.app_manager import app_manager
from core.utils import ImageUtils
from assets.styles import MAIN_STYLE

class MainWindow(QMainWindow):
    """Main application window"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Hệ Thống Điểm Danh Sinh Viên")
        self.setGeometry(0, 0, 1400, 900)
        
        # Apply stylesheet
        self.setStyleSheet(MAIN_STYLE)
        
        # Setup upload directories
        ImageUtils.create_upload_dir()
        
        # Create stacked widget
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)
        
        # Setup windows
        self.login_window = LoginWindow()
        self.teacher_dashboard = TeacherDashboardWindow()
        self.admin_dashboard = AdminDashboardWindow()
        
        # Add windows to stacked widget
        self.stacked_widget.addWidget(self.login_window)
        self.stacked_widget.addWidget(self.teacher_dashboard)
        self.stacked_widget.addWidget(self.admin_dashboard)
        
        # Connect signals
        self.login_window.login_success.connect(self.on_login_success)
        self.teacher_dashboard.logout_requested.connect(self.on_logout)
        self.admin_dashboard.logout_requested.connect(self.on_logout)
        
        # Show login window initially
        self.stacked_widget.setCurrentWidget(self.login_window)
        
        # Load saved tokens
        if auth_manager.load_tokens():
            # Auto-login if tokens exist
            from api.services import AuthAPI  # ✅ SỬA
            ok, user_data = AuthAPI.get_current_user()
            if ok:
                auth_manager.set_current_user(user_data)
                self.show_dashboard(user_data["login"]["level"]["name_level"])
    
    def on_login_success(self, role: str):
        """Handle successful login"""
        self.show_dashboard(role)
    
    def show_dashboard(self, role: str):
        """Show dashboard based on role"""
        if role == "teacher":
            self.stacked_widget.setCurrentWidget(self.teacher_dashboard)
        elif role == "admin":
            self.stacked_widget.setCurrentWidget(self.admin_dashboard)
    
    def on_logout(self):
        """Handle logout"""
        self.login_window.clear_register_form()
        self.login_window.clear_contact_form()
        self.stacked_widget.setCurrentWidget(self.login_window)

def main():
    """Main entry point"""
    app = QApplication(sys.argv)
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()