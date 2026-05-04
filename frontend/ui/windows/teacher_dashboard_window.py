from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QLabel, QTabWidget, QTableWidget, QTableWidgetItem, QLineEdit,
    QComboBox, QMessageBox, QDialog, QFormLayout, QHeaderView
)
from PyQt5.QtCore import Qt, QTimer, pyqtSignal
from PyQt5.QtGui import QFont
from api.services import UserAPI, ClassAPI, AttendanceAPI
from core.utils import DialogUtils, DateTimeUtils
from core.auth_manager import auth_manager

class TeacherDashboardWindow(QMainWindow):
    """Teacher Dashboard Window"""
    
    logout_requested = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Giáo Viên - Hệ Thống Điểm Danh")
        self.setGeometry(100, 100, 1400, 800)
        self.user_data = auth_manager.current_user
        self.init_ui()
        self.setup_timer()
    
    def init_ui(self):
        """Initialize UI"""
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        
        layout = QVBoxLayout()
        
        # Header
        header_layout = QHBoxLayout()
        
        self.time_label = QLabel()
        self.time_label.setFont(QFont("Arial", 10))
        header_layout.addWidget(self.time_label)
        
        header_layout.addStretch()
        
        btn_profile = QPushButton("Xem Thông Tin")
        btn_profile.clicked.connect(self.show_profile)
        header_layout.addWidget(btn_profile)
        
        btn_change_pwd = QPushButton("Đổi Mật Khẩu")
        btn_change_pwd.clicked.connect(self.show_change_password)
        header_layout.addWidget(btn_change_pwd)
        
        btn_messages = QPushButton("Tin Nhắn")
        btn_messages.clicked.connect(self.show_messages)
        header_layout.addWidget(btn_messages)
        
        btn_logout = QPushButton("Đăng Xuất")
        btn_logout.clicked.connect(self.handle_logout)
        header_layout.addWidget(btn_logout)
        
        layout.addLayout(header_layout)
        
        # Tabs
        tabs = QTabWidget()
        tabs.addTab(self.create_classes_tab(), "Quản Lý Lớp Học")
        tabs.addTab(self.create_attendance_tab(), "Điểm Danh")
        tabs.addTab(self.create_face_enrollment_tab(), "Lấy Ảnh Sinh Viên")
        
        layout.addWidget(tabs)
        main_widget.setLayout(layout)
        
        self.update_time()
    
    def setup_timer(self):
        """Setup timer to update time"""
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)
    
    def update_time(self):
        """Update time label"""
        self.time_label.setText(DateTimeUtils.get_current_datetime_string())
    
    def create_classes_tab(self):
        """Create classes management tab"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        # Filter
        filter_layout = QHBoxLayout()
        
        label_course = QLabel("Khóa:")
        self.combo_course = QComboBox()
        filter_layout.addWidget(label_course)
        filter_layout.addWidget(self.combo_course)
        
        label_faculty = QLabel("Khoa:")
        self.combo_faculty = QComboBox()
        filter_layout.addWidget(label_faculty)
        filter_layout.addWidget(self.combo_faculty)
        
        label_status = QLabel("Trạng Thái:")
        self.combo_status = QComboBox()
        self.combo_status.addItems(["ON", "OFF"])
        filter_layout.addWidget(label_status)
        filter_layout.addWidget(self.combo_status)
        
        btn_search = QPushButton("Tìm Kiếm")
        btn_search.clicked.connect(self.search_classes)
        filter_layout.addWidget(btn_search)
        
        filter_layout.addStretch()
        
        layout.addLayout(filter_layout)
        
        # Table
        self.table_classes = QTableWidget()
        self.table_classes.setColumnCount(5)
        self.table_classes.setHorizontalHeaderLabels(["Mã Lớp", "Tên Lớp", "Khoa", "Số SV", "Thao Tác"])
        self.table_classes.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table_classes.itemClicked.connect(self.on_class_selected)
        layout.addWidget(self.table_classes)
        
        widget.setLayout(layout)
        return widget
    
    def create_attendance_tab(self):
        """Create attendance tab"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        label = QLabel("Tab Điểm Danh sẽ được hiển thị ở đây")
        layout.addWidget(label)
        
        widget.setLayout(layout)
        return widget
    
    def create_face_enrollment_tab(self):
        """Create face enrollment tab"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        label = QLabel("Tab Lấy Ảnh Sinh Viên sẽ được hiển thị ở đây")
        layout.addWidget(label)
        
        widget.setLayout(layout)
        return widget
    
    def search_classes(self):
        """Search classes"""
        success, classes = ClassAPI.get_my_classes()
        
        if success and classes:
            self.table_classes.setRowCount(len(classes))
            for row, cls in enumerate(classes):
                self.table_classes.setItem(row, 0, QTableWidgetItem(cls.get("code_class_attendance", "")))
                self.table_classes.setItem(row, 1, QTableWidgetItem(cls.get("name_class_attendance", "")))
                self.table_classes.setItem(row, 2, QTableWidgetItem(str(cls.get("id_faculty", ""))))
                self.table_classes.setItem(row, 3, QTableWidgetItem(str(cls.get("total_students_class_attendance", ""))))
                
                btn_view = QPushButton("Xem Chi Tiết")
                btn_view.clicked.connect(lambda checked, cid=cls["id_class_attendance"]: self.view_class_details(cid))
                self.table_classes.setCellWidget(row, 4, btn_view)
        else:
            DialogUtils.show_warning(self, "Cảnh báo", "Không tìm thấy lớp học")
    
    def view_class_details(self, class_id: int):
        """View class details"""
        DialogUtils.show_info(self, "Thông Báo", f"Viewing class: {class_id}")
    
    def on_class_selected(self, item):
        """Handle class selected"""
        pass
    
    def show_profile(self):
        """Show teacher profile"""
        success, profile = UserAPI.get_my_profile()
        
        if success:
            message = f"Tên: {profile.get('name')}\n"
            message += f"Email: {profile.get('email')}\n"
            message += f"Số ĐT: {profile.get('phone', 'N/A')}"
            DialogUtils.show_info(self, "Thông Tin Cá Nhân", message)
        else:
            DialogUtils.show_error(self, "Lỗi", "Không thể lấy thông tin")
    
    def show_change_password(self):
        """Show change password dialog"""
        dialog = QDialog(self)
        dialog.setWindowTitle("Đổi Mật Khẩu")
        dialog.setGeometry(400, 300, 400, 200)
        
        layout = QFormLayout()
        
        old_pwd = QLineEdit()
        old_pwd.setEchoMode(QLineEdit.Password)
        layout.addRow("Mật Khẩu Cũ:", old_pwd)
        
        new_pwd = QLineEdit()
        new_pwd.setEchoMode(QLineEdit.Password)
        layout.addRow("Mật Khẩu Mới:", new_pwd)
        
        confirm_pwd = QLineEdit()
        confirm_pwd.setEchoMode(QLineEdit.Password)
        layout.addRow("Xác Nhận Mật Khẩu:", confirm_pwd)
        
        btn_layout = QHBoxLayout()
        btn_ok = QPushButton("OK")
        btn_cancel = QPushButton("Hủy")
        btn_layout.addWidget(btn_ok)
        btn_layout.addWidget(btn_cancel)
        layout.addRow(btn_layout)
        
        def on_ok():
            from api.services import AuthAPI
            success, message = AuthAPI.change_password(
                old_pwd.text(), new_pwd.text(), confirm_pwd.text()
            )
            if success:
                DialogUtils.show_info(dialog, "Thành Công", message)
                dialog.close()
            else:
                DialogUtils.show_error(dialog, "Lỗi", message)
        
        btn_ok.clicked.connect(on_ok)
        btn_cancel.clicked.connect(dialog.close)
        
        dialog.setLayout(layout)
        dialog.exec_()
    
    def show_messages(self):
        """Show messages"""
        DialogUtils.show_info(self, "Thông Báo", "Chức năng tin nhắn đang phát triển")
    
    def handle_logout(self):
        """Handle logout"""
        if DialogUtils.ask_question(self, "Xác Nhận", "Bạn có chắc chắn muốn đăng xuất?"):
            from core.auth_manager import auth_manager
            auth_manager.clear_tokens()
            self.logout_requested.emit()