from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QLabel, QTableWidget, QTableWidgetItem, QLineEdit, QHeaderView,
    QMessageBox, QDialog, QFormLayout, QProgressBar, QComboBox
)
from PyQt5.QtCore import Qt, QTimer, pyqtSignal, QThread
from PyQt5.QtGui import QFont, QPixmap
import cv2
import numpy as np
from datetime import datetime
from api.services import ClassAPI
from core.utils import DialogUtils, ImageUtils

class CameraThread(QThread):
    """Thread for camera capture"""
    frame_captured = pyqtSignal(np.ndarray)
    error_occurred = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        self.running = True
        self.cap = None
    
    def run(self):
        """Run camera thread"""
        try:
            self.cap = cv2.VideoCapture(0)
            while self.running and self.cap.isOpened():
                ret, frame = self.cap.read()
                if ret:
                    self.frame_captured.emit(frame)
                else:
                    break
        except Exception as e:
            self.error_occurred.emit(str(e))
    
    def stop(self):
        """Stop camera"""
        self.running = False
        if self.cap:
            self.cap.release()

class FaceEnrollmentWindow(QMainWindow):
    """Face enrollment window for student photo capture"""
    
    close_requested = pyqtSignal()
    
    def __init__(self, class_id: int):
        super().__init__()
        self.class_id = class_id
        self.setWindowTitle("Lấy Ảnh Sinh Viên")
        self.setGeometry(50, 50, 1400, 900)
        self.captured_faces = []
        self.camera_thread = None
        self.init_ui()
        self.load_students()
    
    def init_ui(self):
        """Initialize UI"""
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        
        layout = QVBoxLayout()
        
        # Header
        header_layout = QHBoxLayout()
        self.label_class_info = QLabel("Lớp: ")
        header_layout.addWidget(self.label_class_info)
        header_layout.addStretch()
        
        btn_back = QPushButton("Quay Lại")
        btn_back.clicked.connect(self.handle_close)
        header_layout.addWidget(btn_back)
        
        layout.addLayout(header_layout)
        
        # Main content
        content_layout = QHBoxLayout()
        
        # Left side - Student list
        left_layout = QVBoxLayout()
        
        search_layout = QHBoxLayout()
        self.search_student = QLineEdit()
        self.search_student.setPlaceholderText("Tìm MSSV hoặc tên...")
        btn_search = QPushButton("Tìm")
        btn_search.clicked.connect(self.search_students)
        search_layout.addWidget(self.search_student)
        search_layout.addWidget(btn_search)
        left_layout.addLayout(search_layout)
        
        self.table_students = QTableWidget()
        self.table_students.setColumnCount(4)
        self.table_students.setHorizontalHeaderLabels(["MSSV", "Tên SV", "Trạng Thái", "Thao Tác"])
        self.table_students.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        left_layout.addWidget(self.table_students)
        
        content_layout.addLayout(left_layout, 2)
        
        # Right side - Camera
        right_layout = QVBoxLayout()
        
        right_layout.addWidget(QLabel("Ảnh Sinh Viên:"))
        
        self.label_camera = QLabel()
        self.label_camera.setMinimumSize(300, 300)
        self.label_camera.setStyleSheet("border: 1px solid black;")
        self.label_camera.setAlignment(Qt.AlignCenter)
        self.label_camera.setText("Khởi động Camera...")
        right_layout.addWidget(self.label_camera)
        
        # Controls
        controls_layout = QHBoxLayout()
        
        self.btn_start_camera = QPushButton("Bắt Đầu Camera")
        self.btn_start_camera.clicked.connect(self.start_camera)
        controls_layout.addWidget(self.btn_start_camera)
        
        self.btn_capture = QPushButton("Chụp Ảnh")
        self.btn_capture.clicked.connect(self.capture_photo)
        self.btn_capture.setEnabled(False)
        controls_layout.addWidget(self.btn_capture)
        
        self.btn_stop_camera = QPushButton("Dừng Camera")
        self.btn_stop_camera.clicked.connect(self.stop_camera)
        self.btn_stop_camera.setEnabled(False)
        controls_layout.addWidget(self.btn_stop_camera)
        
        right_layout.addLayout(controls_layout)
        
        # Current student info
        right_layout.addWidget(QLabel("Sinh Viên Hiện Tại:"))
        self.label_current_student = QLabel("Chưa chọn")
        right_layout.addWidget(self.label_current_student)
        
        # Captured faces list
        right_layout.addWidget(QLabel(f"Ảnh Đã Chụp: ({len(self.captured_faces)})"))
        self.label_captured_count = QLabel("0/0")
        right_layout.addWidget(self.label_captured_count)
        
        # Action buttons
        action_layout = QHBoxLayout()
        
        self.btn_train = QPushButton("Train Embedding")
        self.btn_train.clicked.connect(self.train_embeddings)
        action_layout.addWidget(self.btn_train)
        
        self.btn_done = QPushButton("Hoàn Tất")
        self.btn_done.clicked.connect(self.complete_enrollment)
        action_layout.addWidget(self.btn_done)
        
        right_layout.addLayout(action_layout)
        right_layout.addStretch()
        
        content_layout.addLayout(right_layout, 1)
        
        layout.addLayout(content_layout)
        
        main_widget.setLayout(layout)
    
    def load_students(self):
        """Load students for the class"""
        success, class_info = ClassAPI.get_class_info(self.class_id)
        
        if success:
            self.label_class_info.setText(
                f"Lớp: {class_info['class']['name_class_attendance']}"
            )
            students = class_info.get('students', [])
            
            self.table_students.setRowCount(len(students))
            self.all_students = students
            
            for row, student in enumerate(students):
                self.table_students.setItem(row, 0, QTableWidgetItem(
                    student.get('code_student', '')
                ))
                self.table_students.setItem(row, 1, QTableWidgetItem(
                    student.get('name_student', '')
                ))
                
                # Status
                status = "Chưa Có" if row not in self.captured_faces else "Đã Chụp"
                self.table_students.setItem(row, 2, QTableWidgetItem(status))
                
                # Action button
                btn = QPushButton("Chọn")
                btn.clicked.connect(
                    lambda checked, idx=row: self.select_student(idx)
                )
                self.table_students.setCellWidget(row, 3, btn)
    
    def search_students(self):
        """Search students"""
        search_text = self.search_student.text().lower()
        
        for row in range(self.table_students.rowCount()):
            code_item = self.table_students.item(row, 0)
            name_item = self.table_students.item(row, 1)
            
            match = (search_text in code_item.text().lower() or 
                    search_text in name_item.text().lower())
            
            self.table_students.setRowHidden(row, not match)
    
    def select_student(self, student_index: int):
        """Select student"""
        student = self.all_students[student_index]
        self.current_student = student
        self.current_student_index = student_index
        
        self.label_current_student.setText(
            f"{student['code_student']} - {student['name_student']}"
        )
    
    def start_camera(self):
        """Start camera"""
        self.camera_thread = CameraThread()
        self.camera_thread.frame_captured.connect(self.update_frame)
        self.camera_thread.error_occurred.connect(self.handle_camera_error)
        self.camera_thread.start()
        
        self.btn_start_camera.setEnabled(False)
        self.btn_capture.setEnabled(True)
        self.btn_stop_camera.setEnabled(True)
    
    def update_frame(self, frame):
        """Update camera frame"""
        # Convert BGR to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Display on label
        pixmap = ImageUtils.convert_cv_image_to_qpixmap(rgb_frame, 300, 300)
        self.label_camera.setPixmap(pixmap)
    
    def capture_photo(self):
        """Capture photo from camera"""
        if not hasattr(self, 'current_student'):
            DialogUtils.show_warning(self, "Cảnh báo", "Vui lòng chọn sinh viên")
            return
        
        # Simulate photo capture - in real app, get from camera frame
        DialogUtils.show_info(self, "Thành Công", "Ảnh đã được chụp")
        self.captured_faces.append(self.current_student_index)
        self.label_captured_count.setText(f"{len(self.captured_faces)}/∞")
    
    def stop_camera(self):
        """Stop camera"""
        if self.camera_thread:
            self.camera_thread.stop()
            self.camera_thread.wait()
        
        self.btn_start_camera.setEnabled(True)
        self.btn_capture.setEnabled(False)
        self.btn_stop_camera.setEnabled(False)
        self.label_camera.setText("Camera Đã Dừng")
    
    def train_embeddings(self):
        """Train embeddings for captured faces"""
        if not self.captured_faces:
            DialogUtils.show_warning(self, "Cảnh báo", "Chưa chụp ảnh sinh viên nào")
            return
        
        # Simulate training
        progress = QDialog(self)
        progress.setWindowTitle("Đang Xử Lý...")
        progress.setGeometry(500, 500, 400, 100)
        
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Đang tạo embedding..."))
        
        bar = QProgressBar()
        layout.addWidget(bar)
        
        progress.setLayout(layout)
        
        # Simulate progress
        for i in range(101):
            bar.setValue(i)
            progress.update()
            QTimer.singleShot(10, progress.show)
        
        progress.close()
        DialogUtils.show_info(self, "Thành Công", "Embedding đã được tạo")
    
    def complete_enrollment(self):
        """Complete face enrollment"""
        if not self.captured_faces:
            DialogUtils.show_warning(self, "Cảnh báo", "Chưa chụp ảnh sinh viên nào")
            return
        
        success = DialogUtils.ask_question(
            self, "Xác Nhận", 
            f"Lưu {len(self.captured_faces)} ảnh sinh viên?"
        )
        
        if success:
            DialogUtils.show_info(self, "Thành Công", "Ảnh sinh viên đã được lưu")
            self.handle_close()
    
    def handle_camera_error(self, error: str):
        """Handle camera error"""
        DialogUtils.show_error(self, "Lỗi Camera", error)
    
    def handle_close(self):
        """Handle close"""
        self.stop_camera()
        self.close_requested.emit()
        self.close()