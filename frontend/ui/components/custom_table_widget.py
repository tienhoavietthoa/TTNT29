from PyQt5.QtWidgets import (
    QTableWidget, QTableWidgetItem, QPushButton, QHeaderView,
    QAbstractItemView
)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont, QColor

class CustomTableWidget(QTableWidget):
    """Custom table widget with enhanced features"""
    
    row_clicked = pyqtSignal(int, dict)  # row index, row data
    
    def __init__(self, columns: list, parent=None):
        super().__init__(parent)
        self.columns = columns
        self.init_ui()
    
    def init_ui(self):
        """Initialize UI"""
        self.setColumnCount(len(self.columns))
        self.setHorizontalHeaderLabels(self.columns)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.setSelectionMode(QAbstractItemView.SingleSelection)
        self.setAlternatingRowColors(True)
        self.itemClicked.connect(self.on_item_clicked)
    
    def on_item_clicked(self, item):
        """Handle item click"""
        row = item.row()
        row_data = self.get_row_data(row)
        self.row_clicked.emit(row, row_data)
    
    def add_row(self, data: list):
        """Add row to table"""
        row_position = self.rowCount()
        self.insertRow(row_position)
        
        for col, value in enumerate(data):
            if isinstance(value, QPushButton):
                self.setCellWidget(row_position, col, value)
            else:
                item = QTableWidgetItem(str(value))
                self.setItem(row_position, col, item)
    
    def add_rows(self, data_list: list):
        """Add multiple rows"""
        for data in data_list:
            self.add_row(data)
    
    def get_row_data(self, row: int) -> dict:
        """Get row data as dict"""
        data = {}
        for col, column_name in enumerate(self.columns):
            item = self.item(row, col)
            data[column_name] = item.text() if item else ""
        return data
    
    def clear_table(self):
        """Clear all rows"""
        self.setRowCount(0)
    
    def highlight_row(self, row: int, color: QColor = None):
        """Highlight row"""
        if not color:
            color = QColor(255, 255, 0)
        
        for col in range(self.columnCount()):
            item = self.item(row, col)
            if item:
                item.setBackground(color)
    
    def set_row_enabled(self, row: int, enabled: bool):
        """Enable/disable row"""
        for col in range(self.columnCount()):
            item = self.item(row, col)
            if item:
                item.setFlags(item.flags() | Qt.ItemIsEnabled if enabled 
                            else item.flags() & ~Qt.ItemIsEnabled)