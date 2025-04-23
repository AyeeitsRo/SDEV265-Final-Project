import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

from view.main_window import MainWindow
import controller.controller as ctr


class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login Page")
        self.setGeometry(100, 100, 300, 150)
        
        # Obtains screen geometry
        screen = QApplication.primaryScreen()
        screen_geometry = screen.availableGeometry()
        # Calculates position to center the window
        x = (screen_geometry.width() - self.width()) // 2
        y = (screen_geometry.height() - self.height()) // 2
        # Sets the geometry of the window
        self.setGeometry(x, y, self.width(), self.height())
        
        # Set background color
        self.setStyleSheet('background-color: #FAF9F6;') # Off White Color
        
        
        controller = ctr.Controller() # Initializes the controller
        self.main_window = MainWindow(controller) # Initializes the main window


        # Create widgets
        self.username_label = QLabel("Username:")
        self.username_label.setFont(QFont("Roboto", 18))
        self.username_label.setStyleSheet('color: #228B22;')
        self.username_input = QLineEdit()
        self.username_input.setStyleSheet('color: black;')

        self.password_label = QLabel("Password:")
        self.password_label.setFont(QFont("Roboto", 18))
        self.password_label.setStyleSheet('color: #228B22;')
        self.password_input = QLineEdit()
        self.password_input.setStyleSheet('color: black;')
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)

        self.login_button = QPushButton("Login")
        self.login_button.setFont(QFont("Roboto", 18))
        self.login_button.setStyleSheet("""
            background-color: #228B22;
            color: black;
            border-radius: 5px;
            padding: 5px;
        """)
        self.login_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.login_button.clicked.connect(self.handle_login)

        self.status_label = QLabel("")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.username_label)
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)
        layout.addWidget(self.login_button)
        layout.addWidget(self.status_label)

        self.setLayout(layout)

    def handle_login(self):
        username = self.username_input.text()
        password = self.password_input.text()

        # Simple static check for demonstration
        if username == "admin" and password == "1234":
            self.status_label.setText("Login successful!")
            self.main_window.show()
            self.close()
        else:
            self.status_label.setText("Invalid username or password")
