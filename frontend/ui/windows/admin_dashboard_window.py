from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QLabel, QTabWidget, QTableWidget, QTableWidgetItem, QLineEdit,
    QComboBox, QMessageBox, QDialog, QFormLayout, QHeaderView,
    QFileDialog, QSpinBox, QDateEdit, QTimeEdit
)
from PyQt5.QtCore import Qt, QTimer, QDate, QTime, pyqtSignal
from PyQt5.QtGui import QFont
from api.services import UserAPI, ClassAPI, AttendanceAPI
from core.utils import DialogUtils, DateTimeUtils
from core.auth_manager import auth_manager

class AdminDashboardWindow(QMainWindow):
    """Admin Dashboard Window"""
    
    logout_requested = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Admin - Hệ Thống Điểm Danh")
        self.setGeometry(100, 100, 1400, 900)
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
        
        btn_messages = QPushButton("Tin Nhắn")
        btn_messages.clicked.connect(self.show_messages)
        header_layout.addWidget(btn_messages)
        
        btn_logout = QPushButton("Đăng Xuất")
        btn_logout.clicked.connect(self.handle_logout)
        header_layout.addWidget(btn_logout)
        
        layout.addLayout(header_layout)
        
        # Tabs
        tabs = QTabWidget()
        tabs.addTab(self.create_students_tab(), "Quản Lý Sinh Viên")
        tabs.addTab(self.create_classes_tab(), "Quản Lý Lớp Học")
        tabs.addTab(self.create_teachers_tab(), "Quản Lý Giáo Viên")
        tabs.addTab(self.create_contacts_tab(), "Quản Lý Liên Hệ")
        
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
    
    def create_students_tab(self):
        """Create students management tab"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        # Sub-tabs
        sub_tabs = QTabWidget()
        sub_tabs.addTab(self.create_student_statistics_tab(), "Thống Kê")
        sub_tabs.addTab(self.create_student_search_tab(), "Tìm Kiếm")
        sub_tabs.addTab(self.create_student_import_tab(), "Thêm Sinh Viên")
        sub_tabs.addTab(self.create_student_details_tab(), "Chi Tiết")
        
        layout.addWidget(sub_tabs)
        widget.setLayout(layout)
        return widget
    
    def create_student_statistics_tab(self):
        """Create student statistics tab"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        btn_refresh = QPushButton("Làm Mới")
        btn_refresh.clicked.connect(self.load_student_statistics)
        layout.addWidget(btn_refresh)
        
        self.table_student_stats = QTableWidget()
        self.table_student_stats.setColumnCount(5)
        self.table_student_stats.setHorizontalHeaderLabels(
            ["Khóa", "Số Khoa", "Số Sinh Viên", "Thao Tác"]
        )
        self.table_student_stats.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.table_student_stats)
        
        widget.setLayout(layout)
        return widget
    
    def create_student_search_tab(self):
        """Create student search tab"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        # Filters
        filter_layout = QHBoxLayout()
        
        label_course = QLabel("Khóa:")
        self.combo_course_search = QComboBox()
        filter_layout.addWidget(label_course)
        filter_layout.addWidget(self.combo_course_search)
        
        label_faculty = QLabel("Khoa:")
        self.combo_faculty_search = QComboBox()
        filter_layout.addWidget(label_faculty)
        filter_layout.addWidget(self.combo_faculty_search)
        
        label_class = QLabel("Lớp:")
        self.combo_class_search = QComboBox()
        filter_layout.addWidget(label_class)
        filter_layout.addWidget(self.combo_class_search)
        
        btn_search = QPushButton("Tìm Kiếm")
        btn_search.clicked.connect(self.search_students)
        filter_layout.addWidget(btn_search)
        
        btn_all = QPushButton("Hiển Tất Cả")
        btn_all.clicked.connect(self.load_all_students)
        filter_layout.addWidget(btn_all)
        
        layout.addLayout(filter_layout)
        
        # Table
        self.table_students = QTableWidget()
        self.table_students.setColumnCount(8)
        self.table_students.setHorizontalHeaderLabels(
            ["Khóa", "Khoa", "Lớp", "MSSV", "Tên SV", "Ngày Sinh", "Email", "Thao Tác"]
        )
        self.table_students.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.table_students)
        
        widget.setLayout(layout)
        return widget
    
    def create_student_import_tab(self):
        """Create student import tab"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        # Import form
        form_layout = QFormLayout()
        
        self.combo_course_import = QComboBox()
        form_layout.addRow("Khóa:", self.combo_course_import)
        
        self.combo_faculty_import = QComboBox()
        form_layout.addRow("Khoa:", self.combo_faculty_import)
        
        self.combo_class_import = QComboBox()
        form_layout.addRow("Lớp:", self.combo_class_import)
        
        btn_import_layout = QHBoxLayout()
        self.btn_file_import = QPushButton("Chọn File Excel")
        self.btn_file_import.clicked.connect(self.select_student_import_file)
        self.label_file_import = QLabel("Chưa chọn file")
        btn_import_layout.addWidget(self.btn_file_import)
        btn_import_layout.addWidget(self.label_file_import)
        form_layout.addRow("File:", btn_import_layout)
        
        btn_import = QPushButton("Thêm Sinh Viên")
        btn_import.clicked.connect(self.import_students)
        form_layout.addRow(btn_import)
        
        layout.addLayout(form_layout)
        
        # Preview table
        self.table_import_preview = QTableWidget()
        self.table_import_preview.setColumnCount(8)
        self.table_import_preview.setHorizontalHeaderLabels(
            ["Khóa", "Khoa", "Lớp", "MSSV", "Tên SV", "Ngày Sinh", "Email", "SĐT"]
        )
        layout.addWidget(self.table_import_preview)
        
        widget.setLayout(layout)
        return widget
    
    def create_student_details_tab(self):
        """Create student details tab"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        label = QLabel("Chi tiết sinh viên sẽ được hiển thị ở đây")
        layout.addWidget(label)
        
        widget.setLayout(layout)
        return widget
    
    def create_classes_tab(self):
        """Create classes management tab"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        # Sub-tabs
        sub_tabs = QTabWidget()
        sub_tabs.addTab(self.create_classes_list_tab(), "Danh Sách Lớp")
        sub_tabs.addTab(self.create_classes_import_tab(), "Thêm Lớp")
        
        layout.addWidget(sub_tabs)
        widget.setLayout(layout)
        return widget
    
    def create_classes_list_tab(self):
        """Create classes list tab"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        # Filters
        filter_layout = QHBoxLayout()
        
        label_course = QLabel("Khóa:")
        self.combo_course_class = QComboBox()
        filter_layout.addWidget(label_course)
        filter_layout.addWidget(self.combo_course_class)
        
        label_faculty = QLabel("Khoa:")
        self.combo_faculty_class = QComboBox()
        filter_layout.addWidget(label_faculty)
        filter_layout.addWidget(self.combo_faculty_class)
        
        label_status = QLabel("Trạng Thái:")
        self.combo_status_class = QComboBox()
        self.combo_status_class.addItems(["ON", "OFF"])
        filter_layout.addWidget(label_status)
        filter_layout.addWidget(self.combo_status_class)
        
        btn_search = QPushButton("Tìm Kiếm")
        btn_search.clicked.connect(self.search_classes)
        filter_layout.addWidget(btn_search)
        
        filter_layout.addStretch()
        
        layout.addLayout(filter_layout)
        
        # Table
        self.table_classes = QTableWidget()
        self.table_classes.setColumnCount(6)
        self.table_classes.setHorizontalHeaderLabels(
            ["Khóa", "Khoa", "Tên Lớp", "Mã Lớp", "Số SV", "Thao Tác"]
        )
        self.table_classes.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.table_classes)
        
        widget.setLayout(layout)
        return widget
    
    def create_classes_import_tab(self):
        """Create classes import tab"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        # Import form
        form_layout = QFormLayout()
        
        self.combo_course_class_import = QComboBox()
        form_layout.addRow("Khóa:", self.combo_course_class_import)
        
        self.combo_faculty_class_import = QComboBox()
        form_layout.addRow("Khoa:", self.combo_faculty_class_import)
        
        self.combo_teacher_class_import = QComboBox()
        form_layout.addRow("Giáo Viên:", self.combo_teacher_class_import)
        
        btn_import_layout = QHBoxLayout()
        self.btn_file_class_import = QPushButton("Chọn File Excel")
        self.btn_file_class_import.clicked.connect(self.select_class_import_file)
        self.label_file_class_import = QLabel("Chưa chọn file")
        btn_import_layout.addWidget(self.btn_file_class_import)
        btn_import_layout.addWidget(self.label_file_class_import)
        form_layout.addRow("File:", btn_import_layout)
        
        btn_import = QPushButton("Thêm Lớp Học")
        btn_import.clicked.connect(self.import_classes)
        form_layout.addRow(btn_import)
        
        layout.addLayout(form_layout)
        
        # Preview table
        self.table_class_import_preview = QTableWidget()
        self.table_class_import_preview.setColumnCount(7)
        self.table_class_import_preview.setHorizontalHeaderLabels(
            ["Khóa", "Khoa", "Giáo Viên", "Mã Lớp", "Tên Lớp", "Số SV", "Ngày Bắt Đầu"]
        )
        layout.addWidget(self.table_class_import_preview)
        
        widget.setLayout(layout)
        return widget
    
    def create_teachers_tab(self):
        """Create teachers management tab"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        # Sub-tabs
        sub_tabs = QTabWidget()
        sub_tabs.addTab(self.create_teacher_approval_tab(), "Duyệt Tài Khoản")
        sub_tabs.addTab(self.create_teacher_list_tab(), "Danh Sách Giáo Viên")
        
        layout.addWidget(sub_tabs)
        widget.setLayout(layout)
        return widget
    
    def create_teacher_approval_tab(self):
        """Create teacher approval tab"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        btn_refresh = QPushButton("Làm Mới")
        btn_refresh.clicked.connect(self.load_pending_teachers)
        layout.addWidget(btn_refresh)
        
        # Table
        self.table_pending_teachers = QTableWidget()
        self.table_pending_teachers.setColumnCount(5)
        self.table_pending_teachers.setHorizontalHeaderLabels(
            ["Mã GV", "Tên GV", "Email", "Ngày Đăng Ký", "Thao Tác"]
        )
        self.table_pending_teachers.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.table_pending_teachers)
        
        widget.setLayout(layout)
        return widget
    
    def create_teacher_list_tab(self):
        """Create teacher list tab"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        # Search
        search_layout = QHBoxLayout()
        self.search_teacher = QLineEdit()
        self.search_teacher.setPlaceholderText("Tìm kiếm giáo viên...")
        btn_search = QPushButton("Tìm")
        btn_search.clicked.connect(self.search_teachers)
        search_layout.addWidget(self.search_teacher)
        search_layout.addWidget(btn_search)
        layout.addLayout(search_layout)
        
        # Table
        self.table_teachers = QTableWidget()
        self.table_teachers.setColumnCount(4)
        self.table_teachers.setHorizontalHeaderLabels(
            ["Mã GV", "Tên GV", "Tổng Lớp", "Thao Tác"]
        )
        self.table_teachers.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.table_teachers)
        
        widget.setLayout(layout)
        return widget
    
    def create_contacts_tab(self):
        """Create contacts management tab"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        btn_refresh = QPushButton("Làm Mới")
        btn_refresh.clicked.connect(self.load_contacts)
        layout.addWidget(btn_refresh)
        
        # Table
        self.table_contacts = QTableWidget()
        self.table_contacts.setColumnCount(6)
        self.table_contacts.setHorizontalHeaderLabels(
            ["Tên", "Loại", "Email", "SĐT", "Nội Dung", "Ngày"]
        )
        self.table_contacts.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.table_contacts)
        
        widget.setLayout(layout)
        return widget
    
    # Event handlers
    def load_student_statistics(self):
        """Load student statistics"""
        success, stats = UserAPI.get_student_statistics()
        if success and stats:
            self.table_student_stats.setRowCount(len(stats))
            for row, stat in enumerate(stats):
                self.table_student_stats.setItem(row, 0, QTableWidgetItem(stat.get("course_name", "")))
                self.table_student_stats.setItem(row, 1, QTableWidgetItem(str(stat.get("faculties_count", ""))))
                self.table_student_stats.setItem(row, 2, QTableWidgetItem(str(stat.get("students_count", ""))))
                
                btn_view = QPushButton("Xem Chi Tiết")
                self.table_student_stats.setCellWidget(row, 3, btn_view)
    
    def search_students(self):
        """Search students"""
        DialogUtils.show_info(self, "Thông Báo", "Chức năng tìm kiếm đang phát triển")
    
    def load_all_students(self):
        """Load all students"""
        success, students = UserAPI.get_students()
        if success and students:
            self.table_students.setRowCount(len(students))
            for row, student in enumerate(students):
                self.table_students.setItem(row, 3, QTableWidgetItem(student.get("code_student", "")))
                self.table_students.setItem(row, 4, QTableWidgetItem(student.get("name_student", "")))
    
    def select_student_import_file(self):
        """Select file for student import"""
        file_path, _ = QFileDialog.getOpenFileName(self, "Chọn file Excel", "", "Excel Files (*.xlsx)")
        if file_path:
            self.label_file_import.setText(file_path)
            self.student_import_file = file_path
    
    def import_students(self):
        """Import students from file"""
        if not hasattr(self, 'student_import_file'):
            DialogUtils.show_warning(self, "Cảnh báo", "Vui lòng chọn file")
            return
        
        id_course = int(self.combo_course_import.currentData() or 0)
        id_faculty = int(self.combo_faculty_import.currentData() or 0)
        id_class_admin = int(self.combo_class_import.currentData() or 0)
        
        if not all([id_course, id_faculty, id_class_admin]):
            DialogUtils.show_warning(self, "Cảnh báo", "Vui lòng chọn đầy đủ thông tin")
            return
        
        success, message = UserAPI.import_students(
            id_course, id_faculty, id_class_admin, self.student_import_file
        )
        
        if success:
            DialogUtils.show_info(self, "Thành Công", message)
        else:
            DialogUtils.show_error(self, "Lỗi", message)
    
    def search_classes(self):
        """Search classes"""
        DialogUtils.show_info(self, "Thông Báo", "Chức năng tìm kiếm lớp đang phát triển")
    
    def select_class_import_file(self):
        """Select file for class import"""
        file_path, _ = QFileDialog.getOpenFileName(self, "Chọn file Excel", "", "Excel Files (*.xlsx)")
        if file_path:
            self.label_file_class_import.setText(file_path)
            self.class_import_file = file_path
    
    def import_classes(self):
        """Import classes from file"""
        if not hasattr(self, 'class_import_file'):
            DialogUtils.show_warning(self, "Cảnh báo", "Vui lòng chọn file")
            return
        
        DialogUtils.show_info(self, "Thông Báo", "Chức năng import lớp đang phát triển")
    
    def load_pending_teachers(self):
        """Load pending teachers"""
        DialogUtils.show_info(self, "Thông Báo", "Chức năng duyệt giáo viên đang phát triển")
    
    def search_teachers(self):
        """Search teachers"""
        DialogUtils.show_info(self, "Thông Báo", "Chức năng tìm kiếm giáo viên đang phát triển")
    
    def load_contacts(self):
        """Load contacts"""
        DialogUtils.show_info(self, "Thông Báo", "Chức năng liên hệ đang phát triển")
    
    def show_messages(self):
        """Show messages"""
        DialogUtils.show_info(self, "Thông Báo", "Chức năng tin nhắn đang phát triển")
    
    def handle_logout(self):
        """Handle logout"""
        if DialogUtils.ask_question(self, "Xác Nhận", "Bạn có chắc chắn muốn đăng xuất?"):
            auth_manager.clear_tokens()
            self.logout_requested.emit()