import sys
from PyQt6.QtWidgets import QApplication
from database import create_tables
from main_window import MainWindow

if __name__ == "__main__":
    create_tables()
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
