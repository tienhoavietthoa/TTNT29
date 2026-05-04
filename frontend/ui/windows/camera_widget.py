from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout
from PyQt5.QtCore import QTimer, QThread, pyqtSignal, Qt
from PyQt5.QtGui import QPixmap, QImage
import cv2
import numpy as np
from threading import Thread, Lock

class CameraThread(QThread):
    """Thread for continuous camera capture"""
    
    frame_ready = pyqtSignal(np.ndarray)
    error_occurred = pyqtSignal(str)
    
    def __init__(self, camera_id: int = 0):
        super().__init__()
        self.camera_id = camera_id
        self.running = False
        self.cap = None
    
    def run(self):
        """Run camera thread"""
        try:
            self.cap = cv2.VideoCapture(self.camera_id)
            
            if not self.cap.isOpened():
                self.error_occurred.emit("Cannot open camera")
                return
            
            # Set camera properties
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
            self.cap.set(cv2.CAP_PROP_FPS, 30)
            
            self.running = True
            while self.running:
                ret, frame = self.cap.read()
                if ret:
                    self.frame_ready.emit(frame)
                else:
                    break
        
        except Exception as e:
            self.error_occurred.emit(str(e))
        
        finally:
            if self.cap:
                self.cap.release()
    
    def stop(self):
        """Stop camera"""
        self.running = False
        self.wait()

class CameraWidget(QWidget):
    """Camera widget with preview"""
    
    photo_captured = pyqtSignal(np.ndarray)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.camera_thread = None
        self.current_frame = None
        self.frame_lock = Lock()
        self.init_ui()
    
    def init_ui(self):
        """Initialize UI"""
        layout = QVBoxLayout()
        
        # Label for camera preview
        self.label_preview = QLabel()
        self.label_preview.setMinimumSize(480, 360)
        self.label_preview.setStyleSheet("border: 1px solid black; background-color: black;")
        self.label_preview.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label_preview)
        
        # Buttons
        btn_layout = QHBoxLayout()
        
        self.btn_start = QPushButton("Bắt Đầu")
        self.btn_start.clicked.connect(self.start_camera)
        btn_layout.addWidget(self.btn_start)
        
        self.btn_capture = QPushButton("Chụp Ảnh")
        self.btn_capture.clicked.connect(self.capture_photo)
        self.btn_capture.setEnabled(False)
        btn_layout.addWidget(self.btn_capture)
        
        self.btn_stop = QPushButton("Dừng")
        self.btn_stop.clicked.connect(self.stop_camera)
        self.btn_stop.setEnabled(False)
        btn_layout.addWidget(self.btn_stop)
        
        layout.addLayout(btn_layout)
        self.setLayout(layout)
    
    def start_camera(self):
        """Start camera"""
        if self.camera_thread is None or not self.camera_thread.isRunning():
            self.camera_thread = CameraThread()
            self.camera_thread.frame_ready.connect(self.update_frame)
            self.camera_thread.error_occurred.connect(self.on_camera_error)
            self.camera_thread.start()
            
            self.btn_start.setEnabled(False)
            self.btn_capture.setEnabled(True)
            self.btn_stop.setEnabled(True)
    
    def update_frame(self, frame: np.ndarray):
        """Update preview with frame"""
        with self.frame_lock:
            self.current_frame = frame.copy()
        
        # Convert BGR to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_frame.shape
        bytes_per_line = ch * w
        
        # Convert to QImage
        qt_image = QImage(rgb_frame.data, w, h, bytes_per_line, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(qt_image)
        
        # Scale to label size
        scaled_pixmap = pixmap.scaledToWidth(480)
        self.label_preview.setPixmap(scaled_pixmap)
    
    def capture_photo(self):
        """Capture current frame"""
        with self.frame_lock:
            if self.current_frame is not None:
                self.photo_captured.emit(self.current_frame.copy())
    
    def stop_camera(self):
        """Stop camera"""
        if self.camera_thread and self.camera_thread.isRunning():
            self.camera_thread.stop()
            self.label_preview.setText("Camera Đã Dừng")
            self.btn_start.setEnabled(True)
            self.btn_capture.setEnabled(False)
            self.btn_stop.setEnabled(False)
    
    def on_camera_error(self, error: str):
        """Handle camera error"""
        self.label_preview.setText(f"Lỗi: {error}")
        self.btn_start.setEnabled(True)
        self.btn_capture.setEnabled(False)
        self.btn_stop.setEnabled(False)