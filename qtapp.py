import sys

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPalette, QColor
from PyQt6.QtWidgets import (
    QApplication,
    QLabel,
    QMainWindow,
    QPushButton,
    QTabWidget,
    QWidget, QHBoxLayout, QVBoxLayout,
)

from uti260b import Uti260b


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("My App")
        self.thermal = Uti260b()

        layout = QHBoxLayout()

        connection = QVBoxLayout()
        layout.addLayout(connection)

        self.connect_button = QPushButton("📶 Connect")
        self.connect_button.setEnabled(True)
        self.connect_button.clicked.connect(self.connect_clicked)
        connection.addWidget(self.connect_button)

        self.disconnect_button = QPushButton("🚫 Disconnect")
        self.disconnect_button.setEnabled(False)
        connection.addWidget(self.disconnect_button)

        self.connect_status = QLabel("Camera disconnected")
        connection.addWidget(self.connect_status)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def connect_clicked(self):
        self.thermal.find_camera()
        if self.thermal.is_found():
            self.thermal.connect()
            if self.thermal.is_connected():
                self.connect_button.setEnabled(False)
                self.disconnect_button.setEnabled(True)
                self.connect_status.setText("Camera connected")

    def disconnect_clicked(self):
        self.thermal.disconnect()
        if not self.thermal.is_connected():
            self.connect_button.setEnabled(True)
            self.disconnect_button.setEnabled(False)
            self.connect_status.setText("Camera disconnected")


app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()
window.thermal.disconnect()