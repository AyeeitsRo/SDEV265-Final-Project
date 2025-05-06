from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QMessageBox,
    QLineEdit, QPushButton, QVBoxLayout
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QPixmap

from view.main_window import MainWindow
import controller.controller as ctr

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login")
        self.resize(400, 300)  # Slightly bigger window
        
        # Obtains screen geometry
        screen = QApplication.primaryScreen()
        screen_geometry = screen.availableGeometry()
        # Calculates position to center the window
        x = (screen_geometry.width() - self.width()) // 2
        y = (screen_geometry.height() - self.height()) // 2
        # Sets the geometry of the window
        self.setGeometry(x, y, self.width(), self.height())
        
        # === Set background color ===
        self.setStyleSheet("background-color: #FAF9F6;")

        layout = QVBoxLayout()
        
        controller = ctr.Controller() # Initializes the controller
        self.main_window = MainWindow(controller) # Initializes the main window
        
        # === Add Logo ===
        logo_label = QLabel()
        pixmap = QPixmap("resources/company-logo.png")
        pixmap = pixmap.scaledToWidth(150, Qt.TransformationMode.SmoothTransformation)
        logo_label.setPixmap(pixmap)
        logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(logo_label)

        # === Add login fields ===
        input_style = """
            QLineEdit {
                border: 2px solid #228B22;
                border-radius: 5px;
                padding: 6px;
                color: black;
                background-color: white;
            }
        """

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username")
        self.username_input.setStyleSheet(input_style)
        layout.addWidget(self.username_input)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setStyleSheet(input_style)
        layout.addWidget(self.password_input)

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
        layout.addWidget(self.login_button)

        self.setLayout(layout)

    def handle_login(self):
        username = self.username_input.text()
        password = self.password_input.text()

        # Simple static check for demonstration
        if username == "admin" and password == "1234":
            self.main_window.show()
            self.close()
        else:
            msg_box = QMessageBox()
            msg_box.setWindowTitle("Login Failed")
            msg_box.setText("Invalid Username or Password")
            msg_box.setIcon(QMessageBox.Icon.Warning)
            msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
            msg_box.exec()
            
            self.username_input.clear()
            self.password_input.clear()


