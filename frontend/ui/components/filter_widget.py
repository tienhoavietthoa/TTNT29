from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QComboBox, QLineEdit, QPushButton
from PyQt5.QtCore import pyqtSignal

class FilterWidget(QWidget):
    """Reusable filter widget"""
    
    filter_applied = pyqtSignal(dict)
    
    def __init__(self, filters: dict, parent=None):
        super().__init__(parent)
        self.filters = filters
        self.filter_values = {}
        self.init_ui()
    
    def init_ui(self):
        """Initialize UI"""
        layout = QHBoxLayout()
        
        for filter_name, filter_type in self.filters.items():
            layout.addWidget(QLabel(f"{filter_name}:"))
            
            if filter_type == "text":
                widget = QLineEdit()
                widget.setPlaceholderText(f"Nhập {filter_name}...")
            elif filter_type == "select":
                widget = QComboBox()
            
            self.filter_values[filter_name] = widget
            layout.addWidget(widget)
        
        btn_apply = QPushButton("Áp Dụng")
        btn_apply.clicked.connect(self.apply_filters)
        layout.addWidget(btn_apply)
        
        layout.addStretch()
        
        self.setLayout(layout)
    
    def apply_filters(self):
        """Apply filters"""
        data = {}
        for name, widget in self.filter_values.items():
            if hasattr(widget, 'text'):
                data[name] = widget.text()
            elif hasattr(widget, 'currentText'):
                data[name] = widget.currentText()
        
        self.filter_applied.emit(data)
    
    def get_filter_values(self) -> dict:
        """Get current filter values"""
        data = {}
        for name, widget in self.filter_values.items():
            if hasattr(widget, 'text'):
                data[name] = widget.text()
            elif hasattr(widget, 'currentData'):
                data[name] = widget.currentData()
        
        return data
    
    def set_combo_items(self, filter_name: str, items: list):
        """Set items for combo box"""
        if filter_name in self.filter_values:
            widget = self.filter_values[filter_name]
            if hasattr(widget, 'addItems'):
                widget.clear()
                for item in items:
                    if isinstance(item, tuple):
                        widget.addItem(item[0], item[1])
                    else:
                        widget.addItem(str(item))