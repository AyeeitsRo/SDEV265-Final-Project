from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QSizePolicy, QLabel
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QPixmap

class Sidebar(QWidget):
    def __init__(self, window_names, controller, parent=None):
        super().__init__(parent)

        self.controller = controller

        # Create layout for sidebar 
        self.sidebar_layout = QVBoxLayout()
        self.setLayout(self.sidebar_layout)
        self.setFixedWidth(180)
        self.sidebar_layout.setContentsMargins(0, 0, 0, 0)
        self.sidebar_layout.setSpacing(0)

        # Create buttons for each window name
        for window_name in window_names:
            button = QPushButton(window_name)
            button.setStyleSheet("background-color: #228B22; color: black;")
            button.setFixedHeight(40)
            button.setFixedWidth(170)
            button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
            button.setFont(QFont('Roboto', 12))
            self.sidebar_layout.addWidget(button)

            # Connect the button to the controller's corresponding method
            if window_name == "Outgoing Work Orders":
                button.clicked.connect(self.controller.open_order)
            elif window_name == "Order Material":
                button.clicked.connect(self.controller.open_search)
            elif window_name == "Inventory":
                button.clicked.connect(self.controller.open_inventory)
            elif window_name == "Home":
                button.clicked.connect(self.controller.open_home)

        self.sidebar_layout.addStretch()

        # ==== Add Image Above Exit Button ====
        image_label = QLabel()
        pixmap = QPixmap("resources/company-logo.png")  
        pixmap = pixmap.scaled(120, 120, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        image_label.setPixmap(pixmap)
        image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.sidebar_layout.addWidget(image_label)

        # Exit Button
        exit_button = QPushButton("Exit")
        exit_button.setStyleSheet("background-color: #228B22; color: black;")
        exit_button.setFixedHeight(40)
        exit_button.setFixedWidth(170)
        exit_button.setFont(QFont('Roboto', 12))
        self.sidebar_layout.addWidget(exit_button)
        exit_button.clicked.connect(self.controller.exit_app)

        # Align buttons to the top
        self.sidebar_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
