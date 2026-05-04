from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QTabWidget, QFrame, QFormLayout,
    QComboBox, QTextEdit, QMessageBox
)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont, QPixmap
from api.services import AuthAPI, ContactAPI
from core.utils import DialogUtils, ValidationUtils
from core.auth_manager import auth_manager

class LoginWindow(QMainWindow):
    """Login Window with Register, Contact tabs"""
    
    login_success = pyqtSignal(str)  # Emit role (teacher/admin)
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Hệ Thống Điểm Danh - Đăng Nhập")
        self.setGeometry(100, 100, 600, 500)
        self.init_ui()
    
    def init_ui(self):
        """Initialize UI"""
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        
        layout = QVBoxLayout()
        
        # Title
        title = QLabel("Hệ Thống Điểm Danh Sinh Viên")
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Tab Widget
        tabs = QTabWidget()
        tabs.addTab(self.create_login_tab(), "Đăng Nhập")
        tabs.addTab(self.create_register_tab(), "Đăng Ký Giáo Viên")
        tabs.addTab(self.create_student_attendance_tab(), "Xem Điểm Danh")
        tabs.addTab(self.create_contact_tab(), "Liên Hệ")
        
        layout.addWidget(tabs)
        main_widget.setLayout(layout)
    
    def create_login_tab(self):
        """Create login tab"""
        widget = QWidget()
        layout = QFormLayout()
        
        self.login_code = QLineEdit()
        self.login_code.setPlaceholderText("Mã giáo viên hoặc admin")
        layout.addRow("Mã Đăng Nhập:", self.login_code)
        
        self.login_password = QLineEdit()
        self.login_password.setEchoMode(QLineEdit.Password)
        layout.addRow("Mật Khẩu:", self.login_password)
        
        btn_layout = QHBoxLayout()
        btn_login = QPushButton("Đăng Nhập")
        btn_login.clicked.connect(self.handle_login)
        btn_layout.addWidget(btn_login)
        
        layout.addRow(btn_layout)
        
        widget.setLayout(layout)
        return widget
    
    def create_register_tab(self):
        """Create register tab"""
        widget = QWidget()
        layout = QFormLayout()
        
        self.reg_code = QLineEdit()
        layout.addRow("Mã Giáo Viên:", self.reg_code)
        
        self.reg_name = QLineEdit()
        layout.addRow("Tên Giáo Viên:", self.reg_name)
        
        self.reg_email = QLineEdit()
        layout.addRow("Email:", self.reg_email)
        
        self.reg_phone = QLineEdit()
        layout.addRow("Số Điện Thoại:", self.reg_phone)
        
        self.reg_password = QLineEdit()
        self.reg_password.setEchoMode(QLineEdit.Password)
        layout.addRow("Mật Khẩu:", self.reg_password)
        
        self.reg_confirm_password = QLineEdit()
        self.reg_confirm_password.setEchoMode(QLineEdit.Password)
        layout.addRow("Xác Nhận Mật Khẩu:", self.reg_confirm_password)
        
        btn_layout = QHBoxLayout()
        btn_register = QPushButton("Đăng Ký")
        btn_register.clicked.connect(self.handle_register)
        btn_layout.addWidget(btn_register)
        
        layout.addRow(btn_layout)
        
        widget.setLayout(layout)
        return widget
    
    def create_student_attendance_tab(self):
        """Create student attendance view tab"""
        widget = QWidget()
        layout = QFormLayout()
        
        self.student_code = QLineEdit()
        layout.addRow("Mã Sinh Viên:", self.student_code)
        
        self.class_code = QLineEdit()
        layout.addRow("Mã Lớp:", self.class_code)
        
        btn_layout = QHBoxLayout()
        btn_search = QPushButton("Tìm Kiếm")
        btn_search.clicked.connect(self.handle_search_attendance)
        btn_layout.addWidget(btn_search)
        
        layout.addRow(btn_layout)
        
        widget.setLayout(layout)
        return widget
    
    def create_contact_tab(self):
        """Create contact tab"""
        widget = QWidget()
        layout = QFormLayout()
        
        self.contact_name = QLineEdit()
        layout.addRow("Tên:", self.contact_name)
        
        self.contact_type = QComboBox()
        self.contact_type.addItems(["teacher", "student", "other"])
        layout.addRow("Loại:", self.contact_type)
        
        self.contact_email = QLineEdit()
        layout.addRow("Email:", self.contact_email)
        
        self.contact_phone = QLineEdit()
        layout.addRow("Số Điện Thoại:", self.contact_phone)
        
        self.contact_content = QTextEdit()
        layout.addRow("Nội Dung:", self.contact_content)
        
        btn_layout = QHBoxLayout()
        btn_send = QPushButton("Gửi")
        btn_send.clicked.connect(self.handle_send_contact)
        btn_layout.addWidget(btn_send)
        
        layout.addRow(btn_layout)
        
        widget.setLayout(layout)
        return widget
    
    def handle_login(self):
        """Handle login"""
        code = self.login_code.text().strip()
        password = self.login_password.text()
        
        if not code or not password:
            DialogUtils.show_warning(self, "Cảnh báo", "Vui lòng nhập đầy đủ thông tin")
            return
        
        success, message = AuthAPI.login(code, password)
        
        if success:
            # Get user info
            ok, user_data = AuthAPI.get_current_user()
            if ok:
                auth_manager.set_current_user(user_data)
                role = user_data["login"]["level"]["name_level"]
                self.login_success.emit(role)
            else:
                DialogUtils.show_error(self, "Lỗi", "Không thể lấy thông tin người dùng")
        else:
            DialogUtils.show_error(self, "Lỗi Đăng Nhập", message)
    
    def handle_register(self):
        """Handle register"""
        code = self.reg_code.text().strip()
        name = self.reg_name.text().strip()
        email = self.reg_email.text().strip()
        phone = self.reg_phone.text().strip()
        password = self.reg_password.text()
        confirm = self.reg_confirm_password.text()
        
        # Validation
        if not all([code, name, email, password, confirm]):
            DialogUtils.show_warning(self, "Cảnh báo", "Vui lòng nhập đầy đủ thông tin")
            return
        
        if not ValidationUtils.validate_email(email):
            DialogUtils.show_warning(self, "Cảnh báo", "Email không hợp lệ")
            return
        
        if password != confirm:
            DialogUtils.show_warning(self, "Cảnh báo", "Mật khẩu không trùng khớp")
            return
        
        success, message = AuthAPI.register_teacher(code, name, email, password, confirm, phone)
        
        if success:
            DialogUtils.show_info(self, "Thành Công", message)
            self.clear_register_form()
        else:
            DialogUtils.show_error(self, "Lỗi Đăng Ký", message)
    
    def handle_search_attendance(self):
        """Handle search attendance"""
        code = self.student_code.text().strip()
        class_code = self.class_code.text().strip()
        
        if not code or not class_code:
            DialogUtils.show_warning(self, "Cảnh báo", "Vui lòng nhập đầy đủ thông tin")
            return
        
        # TODO: Navigate to attendance view
        DialogUtils.show_info(self, "Thông Báo", "Chức năng này sẽ được cập nhật")
    
    def handle_send_contact(self):
        """Handle send contact"""
        name = self.contact_name.text().strip()
        contact_type = self.contact_type.currentText()
        email = self.contact_email.text().strip()
        phone = self.contact_phone.text().strip()
        content = self.contact_content.toPlainText().strip()
        
        if not all([name, email, content]):
            DialogUtils.show_warning(self, "Cảnh báo", "Vui lòng nhập đầy đủ thông tin")
            return
        
        if not ValidationUtils.validate_email(email):
            DialogUtils.show_warning(self, "Cảnh báo", "Email không hợp lệ")
            return
        
        success, message = ContactAPI.submit_contact(name, contact_type, email, phone, content)
        
        if success:
            DialogUtils.show_info(self, "Thành Công", message)
            self.clear_contact_form()
        else:
            DialogUtils.show_error(self, "Lỗi", message)
    
    def clear_register_form(self):
        """Clear register form"""
        self.reg_code.clear()
        self.reg_name.clear()
        self.reg_email.clear()
        self.reg_phone.clear()
        self.reg_password.clear()
        self.reg_confirm_password.clear()
    
    def clear_contact_form(self):
        """Clear contact form"""
        self.contact_name.clear()
        self.contact_email.clear()
        self.contact_phone.clear()
        self.contact_content.clear()