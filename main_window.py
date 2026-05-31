import sys
from PyQt6.QtWidgets import *
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor
from database import *

class AddTripDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("إضافة رحلة جديدة")
        self.setModal(True)
        self.setFixedSize(400, 350)
        layout = QVBoxLayout()
        layout.addWidget(QLabel("اسم الزبون:"))
        self.customer_name = QLineEdit()
        layout.addWidget(self.customer_name)
        layout.addWidget(QLabel("اسم السائق:"))
        self.driver_name = QLineEdit()
        layout.addWidget(self.driver_name)
        layout.addWidget(QLabel("وصف الرحلة:"))
        self.trip_description = QLineEdit()
        layout.addWidget(self.trip_description)
        layout.addWidget(QLabel("تكلفة الرحلة:"))
        self.trip_cost = QLineEdit()
        layout.addWidget(self.trip_cost)
        layout.addWidget(QLabel("تاريخ الرحلة (YYYY-MM-DD):"))
        self.trip_date = QLineEdit()
        layout.addWidget(self.trip_date)
        self.is_paid = QCheckBox("مدفوع")
        layout.addWidget(self.is_paid)
        btn = QPushButton("إضافة")
        btn.clicked.connect(self.accept)
        layout.addWidget(btn)
        self.setLayout(layout)
    
    def get_data(self):
        return (self.customer_name.text(), self.driver_name.text(), 
                self.trip_description.text(), float(self.trip_cost.text() or 0),
                self.trip_date.text(), 1 if self.is_paid.isChecked() else 0)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("نظام إدارة سيارات الأجرة")
        self.setGeometry(100, 100, 1000, 500)
        self.selected_id = None
        widget = QWidget()
        self.setCentralWidget(widget)
        layout = QVBoxLayout(widget)
        btn_layout = QHBoxLayout()
        btn_add = QPushButton("➕ إضافة رحلة")
        btn_add.clicked.connect(self.add_trip)
        btn_layout.addWidget(btn_add)
        btn_delete = QPushButton("🗑️ حذف")
        btn_delete.clicked.connect(self.delete_trip)
        btn_layout.addWidget(btn_delete)
        btn_unmark = QPushButton("⚪ إزالة التمييز")
        btn_unmark.clicked.connect(self.remove_highlight)
        btn_layout.addWidget(btn_unmark)
        btn_refresh = QPushButton("🔄 تحديث")
        btn_refresh.clicked.connect(self.load_trips)
        btn_layout.addWidget(btn_refresh)
        layout.addLayout(btn_layout)
        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels(["ID", "السائق", "الزبون", "الوصف", "التكلفة", "التاريخ", "مدفوع"])
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.itemClicked.connect(self.on_row_click)
        layout.addWidget(self.table)
        self.status = QLabel("جاهز")
        layout.addWidget(self.status)
        self.load_trips()
    
    def load_trips(self):
        trips = get_all_trips()
        self.table.setRowCount(len(trips))
        highlighted = get_highlighted_trips()
        for i, trip in enumerate(trips):
            for j in range(6):
                item = QTableWidgetItem(str(trip[j+1]))
                if trip[0] in highlighted:
                    item.setBackground(QColor(200, 200, 200))
                self.table.setItem(i, j, item)
            paid = QTableWidgetItem("نعم" if trip[6] == 1 else "لا")
            if trip[0] in highlighted:
                paid.setBackground(QColor(200, 200, 200))
            self.table.setItem(i, 6, paid)
        self.status.setText(f"{len(trips)} رحلة")
    
    def on_row_click(self, item):
        row = item.row()
        self.selected_id = int(self.table.item(row, 0).text())
        set_highlight(self.selected_id, True)
        self.load_trips()
        self.status.setText(f"تم تمييز الرحلة {self.selected_id}")
    
    def remove_highlight(self):
        if self.selected_id:
            set_highlight(self.selected_id, False)
            self.load_trips()
            self.status.setText("تم إزالة التمييز")
    
    def add_trip(self):
        dlg = AddTripDialog(self)
        if dlg.exec():
            data = dlg.get_data()
            add_trip(*data)
            self.load_trips()
            QMessageBox.information(self, "تم", "تم إضافة الرحلة")
    
    def delete_trip(self):
        if self.selected_id:
            reply = QMessageBox.question(self, "تأكيد", "احذف الرحلة؟", QMessageBox.Yes | QMessageBox.No)
            if reply == QMessageBox.Yes:
                delete_trip(self.selected_id)
                self.selected_id = None
                self.load_trips()
