from PyQt6.QtWidgets import QApplication
from weather_app.ui.main_window import MainWindow
import sys

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.resize(1000, 800)
    window.show()
    sys.exit(app.exec())
