from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QLabel, QListWidget, QListWidgetItem, QTextEdit, QLineEdit,
    QHeaderView, QDialog, QFormLayout
)
from PyQt5.QtCore import Qt, QTimer, pyqtSignal
from PyQt5.QtGui import QFont
from api.services import MessageAPI
from core.utils import DialogUtils, DateTimeUtils

class MessageWindow(QMainWindow):
    """Message window for teacher/admin communication"""
    
    close_requested = pyqtSignal()
    
    def __init__(self, current_login_id: int):
        super().__init__()
        self.current_login_id = current_login_id
        self.setWindowTitle("Tin Nhắn")
        self.setGeometry(200, 200, 1000, 600)
        self.selected_user_id = None
        self.init_ui()
        self.load_conversations()
        self.setup_refresh_timer()
    
    def init_ui(self):
        """Initialize UI"""
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        
        layout = QHBoxLayout()
        
        # Left side - Conversations list
        left_layout = QVBoxLayout()
        
        left_layout.addWidget(QLabel("Cuộc Trò Chuyện:"))
        
        self.list_conversations = QListWidget()
        self.list_conversations.itemClicked.connect(self.on_conversation_selected)
        left_layout.addWidget(self.list_conversations)
        
        # Add new conversation button
        btn_new = QPushButton("Tin Nhắn Mới")
        btn_new.clicked.connect(self.show_new_conversation_dialog)
        left_layout.addWidget(btn_new)
        
        layout.addLayout(left_layout, 1)
        
        # Right side - Chat area
        right_layout = QVBoxLayout()
        
        self.label_conversation_title = QLabel("Chọn cuộc trò chuyện")
        self.label_conversation_title.setFont(QFont("Arial", 11, QFont.Bold))
        right_layout.addWidget(self.label_conversation_title)
        
        # Messages display
        self.text_messages = QTextEdit()
        self.text_messages.setReadOnly(True)
        right_layout.addWidget(self.text_messages)
        
        # Input area
        input_layout = QHBoxLayout()
        self.text_input = QLineEdit()
        self.text_input.setPlaceholderText("Nhập tin nhắn...")
        btn_send = QPushButton("Gửi")
        btn_send.clicked.connect(self.send_message)
        input_layout.addWidget(self.text_input)
        input_layout.addWidget(btn_send)
        right_layout.addLayout(input_layout)
        
        layout.addLayout(right_layout, 2)
        
        main_widget.setLayout(layout)
    
    def setup_refresh_timer(self):
        """Setup timer to refresh messages"""
        self.timer = QTimer()
        self.timer.timeout.connect(self.refresh_messages)
        self.timer.start(5000)  # Refresh every 5 seconds
    
    def load_conversations(self):
        """Load all conversations"""
        success, conversations = MessageAPI.get_my_conversations()
        
        self.list_conversations.clear()
        
        if success and conversations:
            for user_id, message in conversations.items():
                # Get user name from message (simplified)
                item_text = f"User {user_id}"
                item = QListWidgetItem(item_text)
                item.setData(Qt.UserRole, user_id)
                self.list_conversations.addItem(item)
    
    def on_conversation_selected(self, item: QListWidgetItem):
        """Handle conversation selected"""
        self.selected_user_id = item.data(Qt.UserRole)
        self.label_conversation_title.setText(f"Trò chuyện với User {self.selected_user_id}")
        self.load_conversation_messages()
    
    def load_conversation_messages(self):
        """Load messages for selected conversation"""
        if not self.selected_user_id:
            return
        
        success, messages = MessageAPI.get_conversation(self.selected_user_id)
        
        self.text_messages.clear()
        
        if success and messages:
            for msg in messages:
                sender = "Bạn" if msg['sender_id_login'] == self.current_login_id else "Họ"
                time_str = DateTimeUtils.format_datetime(msg['sent_at_message'])
                
                message_text = f"[{time_str}] {sender}:\n{msg['content_message']}\n\n"
                self.text_messages.append(message_text)
    
    def refresh_messages(self):
        """Refresh messages if conversation is selected"""
        if self.selected_user_id:
            self.load_conversation_messages()
    
    def send_message(self):
        """Send message"""
        if not self.selected_user_id:
            DialogUtils.show_warning(self, "Cảnh báo", "Vui lòng chọn cuộc trò chuyện")
            return
        
        content = self.text_input.text().strip()
        if not content:
            return
        
        success, message = MessageAPI.send_message(self.selected_user_id, content)
        
        if success:
            self.text_input.clear()
            self.load_conversation_messages()
        else:
            DialogUtils.show_error(self, "Lỗi", message)
    
    def show_new_conversation_dialog(self):
        """Show new conversation dialog"""
        dialog = QDialog(self)
        dialog.setWindowTitle("Tin Nhắn Mới")
        dialog.setGeometry(400, 400, 400, 150)
        
        layout = QFormLayout()
        
        label_user = QLabel("ID Người Dùng:")
        text_user_id = QLineEdit()
        layout.addRow(label_user, text_user_id)
        
        btn_layout = QHBoxLayout()
        btn_ok = QPushButton("OK")
        btn_cancel = QPushButton("Hủy")
        btn_layout.addWidget(btn_ok)
        btn_layout.addWidget(btn_cancel)
        layout.addRow(btn_layout)
        
        def on_ok():
            try:
                user_id = int(text_user_id.text())
                self.selected_user_id = user_id
                self.label_conversation_title.setText(f"Trò chuyện với User {user_id}")
                self.load_conversation_messages()
                dialog.close()
            except ValueError:
                DialogUtils.show_warning(dialog, "Cảnh báo", "ID người dùng không hợp lệ")
        
        btn_ok.clicked.connect(on_ok)
        btn_cancel.clicked.connect(dialog.close)
        
        dialog.setLayout(layout)
        dialog.exec_()
    
    def closeEvent(self, event):
        """Handle close event"""
        self.timer.stop()
        self.close_requested.emit()
        super().closeEvent(event)