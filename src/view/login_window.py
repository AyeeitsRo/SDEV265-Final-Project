from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QMessageBox,
    QLineEdit, QPushButton, QVBoxLayout
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QPixmap

from view.main_window import MainWindow  
import controller.controller as ctr 


class LoginWindow(QWidget):
    """
    LoginWindow Class

    Represents the login screen. Displays input fields for username/password,
    a logo, and a login button. On successful login, shows the main window.
    """

    def __init__(self) -> None:
        """
        Initialize the login window and its components.
        """
        super().__init__()

        self.setWindowTitle("Login") 
        self.resize(400, 300)         

        # === Center the login window on the screen ===
        screen = QApplication.primaryScreen()
        screen_geometry = screen.availableGeometry()
        x: int = (screen_geometry.width() - self.width()) // 2
        y: int = (screen_geometry.height() - self.height()) // 2
        self.setGeometry(x, y, self.width(), self.height())

        # Set background color for the login window
        self.setStyleSheet("background-color: #FAF9F6;")

        # === Main vertical layout ===
        layout: QVBoxLayout = QVBoxLayout()

        # === Create controller and initialize the main dashboard window ===
        controller: ctr.Controller = ctr.Controller()
        self.main_window: MainWindow = MainWindow(controller)

        # === Logo Display ===
        logo_label: QLabel = QLabel()  # QLabel to hold the logo image
        pixmap: QPixmap = QPixmap("resources/company-logo.png")  # Load the image file
        pixmap = pixmap.scaledToWidth(150, Qt.TransformationMode.SmoothTransformation)  # Scale for consistency
        logo_label.setPixmap(pixmap)
        logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Center the image
        layout.addWidget(logo_label)

        # === Style for text input fields ===
        input_style: str = """
            QLineEdit {
                border: 2px solid #228B22;
                border-radius: 5px;
                padding: 6px;
                color: black;
                background-color: white;
            }
        """

        # === Username Field ===
        self.username_input: QLineEdit = QLineEdit()
        self.username_input.setPlaceholderText("Username")  # Hint text inside field
        self.username_input.setStyleSheet(input_style)      # Apply custom style
        layout.addWidget(self.username_input)

        # === Password Field ===
        self.password_input: QLineEdit = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)  # Hide password input
        self.password_input.setStyleSheet(input_style)
        layout.addWidget(self.password_input)

        # === Login Button ===
        self.login_button: QPushButton = QPushButton("Login")
        self.login_button.setFont(QFont("Roboto", 18))  # Font for the button text
        self.login_button.setStyleSheet("""
            background-color: #228B22;
            color: black;
            border-radius: 5px;
            padding: 5px;
        """)
        self.login_button.setCursor(Qt.CursorShape.PointingHandCursor)  # Change cursor on hover
        self.login_button.clicked.connect(self.handle_login)            # Connect button to login logic
        layout.addWidget(self.login_button)

        # Set the layout to the window
        self.setLayout(layout)

    def handle_login(self) -> None:
        """
        Check login credentials and either show the main window or show an error dialog.
        """
        username: str = self.username_input.text()
        password: str = self.password_input.text()

        # === Check credentials ===
        if username == "admin" and password == "1234":
            # If correct, open the main window and close login
            self.main_window.show()
            self.close()
        else:
            # If incorrect, show a warning message
            msg_box: QMessageBox = QMessageBox()
            msg_box.setWindowTitle("Login Failed")
            msg_box.setText("Invalid Username or Password")
            msg_box.setIcon(QMessageBox.Icon.Warning)
            msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
            msg_box.exec()

            # Clear input fields after failed login
            self.username_input.clear()
            self.password_input.clear()
