from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QLabel, QTableWidget, QTableWidgetItem, QLineEdit, QHeaderView,
    QMessageBox, QDialog, QFormLayout, QTextEdit, QComboBox
)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont, QPixmap
from api.services import AttendanceAPI, ClassAPI
from core.utils import DialogUtils, DateTimeUtils, ImageUtils

class AttendanceDetailWindow(QMainWindow):
    """Detailed attendance marking window"""
    
    close_requested = pyqtSignal()
    
    def __init__(self, class_id: int, session_id: int = None):
        super().__init__()
        self.class_id = class_id
        self.session_id = session_id
        self.setWindowTitle("Chi Tiết Điểm Danh")
        self.setGeometry(100, 100, 1400, 800)
        self.init_ui()
        self.load_data()
    
    def init_ui(self):
        """Initialize UI"""
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        
        layout = QVBoxLayout()
        
        # Header with class info
        header_layout = QHBoxLayout()
        
        self.label_class_info = QLabel()
        self.label_class_info.setFont(QFont("Arial", 11, QFont.Bold))
        header_layout.addWidget(self.label_class_info)
        
        header_layout.addStretch()
        
        self.label_session_info = QLabel()
        header_layout.addWidget(self.label_session_info)
        
        btn_back = QPushButton("Quay Lại")
        btn_back.clicked.connect(self.handle_close)
        header_layout.addWidget(btn_back)
        
        layout.addLayout(header_layout)
        
        # Session selector if needed
        if not self.session_id:
            session_layout = QHBoxLayout()
            label = QLabel("Chọn Buổi Học:")
            self.combo_sessions = QComboBox()
            self.combo_sessions.currentIndexChanged.connect(self.on_session_changed)
            session_layout.addWidget(label)
            session_layout.addWidget(self.combo_sessions)
            session_layout.addStretch()
            layout.addLayout(session_layout)
        
        # Statistics
        stats_layout = QHBoxLayout()
        self.label_total = QLabel("Tổng: 0")
        self.label_present = QLabel("Có Mặt: 0")
        self.label_absent = QLabel("Vắng: 0")
        stats_layout.addWidget(self.label_total)
        stats_layout.addWidget(self.label_present)
        stats_layout.addWidget(self.label_absent)
        stats_layout.addStretch()
        layout.addLayout(stats_layout)
        
        # Attendance table
        self.table_attendance = QTableWidget()
        self.table_attendance.setColumnCount(6)
        self.table_attendance.setHorizontalHeaderLabels(
            ["MSSV", "Tên SV", "Trạng Thái", "Giờ Điểm Danh", "Ảnh", "Thao Tác"]
        )
        self.table_attendance.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.table_attendance)
        
        main_widget.setLayout(layout)
    
    def load_data(self):
        """Load attendance data"""
        # Get class info
        success, class_info = ClassAPI.get_class_info(self.class_id)
        if success:
            self.label_class_info.setText(
                f"Lớp: {class_info['class']['name_class_attendance']} "
                f"({class_info['class']['code_class_attendance']})"
            )
        
        # Load sessions
        if not self.session_id and success:
            sessions = class_info.get('sessions', [])
            for session in sessions:
                self.combo_sessions.addItem(
                    f"Buổi {session['session_number']} - {session['session_date']}",
                    session['id_session_attendance']
                )
    
    def on_session_changed(self):
        """Handle session change"""
        if self.combo_sessions.count() > 0:
            self.session_id = self.combo_sessions.currentData()
            self.load_attendance_data()
    
    def load_attendance_data(self):
        """Load attendance data for selected session"""
        if not self.session_id:
            return
        
        success, session_data = AttendanceAPI.get_session_details(self.session_id)
        
        if success:
            session = session_data['session']
            stats = session_data['stats']
            attendances = session_data['attendances']
            
            # Update info
            self.label_session_info.setText(
                f"Tiết: {session['session_start_hour']} - {session['session_end_hour']} | "
                f"Ngày: {session['session_date']}"
            )
            
            # Update statistics
            self.label_total.setText(f"Tổng: {stats['total']}")
            self.label_present.setText(f"Có Mặt: {stats['present']}")
            self.label_absent.setText(f"Vắng: {stats['absent']}")
            
            # Fill table
            self.table_attendance.setRowCount(len(attendances))
            for row, attendance in enumerate(attendances):
                student = attendance.get('student', {})
                
                self.table_attendance.setItem(row, 0, QTableWidgetItem(
                    student.get('code_student', '')
                ))
                self.table_attendance.setItem(row, 1, QTableWidgetItem(
                    student.get('name_student', '')
                ))
                self.table_attendance.setItem(row, 2, QTableWidgetItem(
                    attendance.get('status_attendance', 'Chưa DD')
                ))
                self.table_attendance.setItem(row, 3, QTableWidgetItem(
                    attendance.get('checkin_time_attendance', '') or '-'
                ))
                
                # Image button
                if attendance.get('img_filename_attendance'):
                    btn_img = QPushButton("Xem Ảnh")
                    btn_img.clicked.connect(
                        lambda checked, img=attendance['img_filename_attendance']: 
                        self.show_attendance_image(img)
                    )
                    self.table_attendance.setCellWidget(row, 4, btn_img)
                
                # Action button
                status = attendance.get('status_attendance', '')
                if status == 'absent' or not status:
                    btn_manual = QPushButton("Điểm Danh Thủ Công")
                    btn_manual.clicked.connect(
                        lambda checked, aid=attendance['id_attendance']: 
                        self.show_manual_checkin_dialog(aid, student.get('id_student'))
                    )
                    self.table_attendance.setCellWidget(row, 5, btn_manual)
    
    def show_attendance_image(self, img_filename: str):
        """Show attendance image"""
        dialog = QDialog(self)
        dialog.setWindowTitle("Ảnh Điểm Danh")
        dialog.setGeometry(300, 300, 500, 600)
        
        layout = QVBoxLayout()
        
        # Load and display image
        pixmap = ImageUtils.load_image_as_qpixmap(f"uploads/{img_filename}", 400, 500)
        label_img = QLabel()
        label_img.setPixmap(pixmap)
        layout.addWidget(label_img)
        
        btn_close = QPushButton("Đóng")
        btn_close.clicked.connect(dialog.close)
        layout.addWidget(btn_close)
        
        dialog.setLayout(layout)
        dialog.exec_()
    
    def show_manual_checkin_dialog(self, attendance_id: int, student_id: int):
        """Show manual checkin dialog"""
        dialog = QDialog(self)
        dialog.setWindowTitle("Điểm Danh Thủ Công")
        dialog.setGeometry(400, 400, 400, 200)
        
        layout = QFormLayout()
        
        label_reason = QLabel("Lý Do:")
        text_reason = QTextEdit()
        layout.addRow(label_reason, text_reason)
        
        btn_layout = QHBoxLayout()
        btn_save = QPushButton("Lưu")
        btn_cancel = QPushButton("Hủy")
        btn_layout.addWidget(btn_save)
        btn_layout.addWidget(btn_cancel)
        layout.addRow(btn_layout)
        
        def on_save():
            reason = text_reason.toPlainText().strip()
            if not reason:
                DialogUtils.show_warning(dialog, "Cảnh báo", "Vui lòng nhập lý do")
                return
            
            success, message = AttendanceAPI.manual_checkin_student(
                self.session_id, self.class_id, student_id, reason
            )
            
            if success:
                DialogUtils.show_info(dialog, "Thành Công", message)
                self.load_attendance_data()
                dialog.close()
            else:
                DialogUtils.show_error(dialog, "Lỗi", message)
        
        btn_save.clicked.connect(on_save)
        btn_cancel.clicked.connect(dialog.close)
        
        dialog.setLayout(layout)
        dialog.exec_()
    
    def handle_close(self):
        """Handle close"""
        self.close_requested.emit()
        self.close()