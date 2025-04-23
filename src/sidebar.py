from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QSizePolicy
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

class Sidebar(QWidget):
    def __init__(self, window_names, controller, parent=None):
        super().__init__(parent)

        self.controller = controller

        # Create layout for sidebar 
        self.sidebar_layout = QVBoxLayout()
        self.setLayout(self.sidebar_layout)
        #self.setFixedWidth(180)
        self.sidebar_layout.setContentsMargins(0, 0, 0, 0)
        self.sidebar_layout.setSpacing(0)

        
        # Create buttons for each window name
        for window_name in window_names:
            button = QPushButton(window_name)
            # Button styling (off-white background and black text)
            button.setStyleSheet("background-color: #FAF9F6; color: black;") # Sets background color of buttons to green and button text to black
            button.setFixedHeight(40) # Set a fixed height for each button
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
        
        # Create Exit button on bottom of sidebar
        exit_button = QPushButton("Exit")
        exit_button.setStyleSheet("background-color: #FAF9F6; color: black;")
        exit_button.setFixedHeight(40)
        exit_button.setFixedWidth(170)
        exit_button.setFont(QFont('Roboto', 12))
        self.sidebar_layout.addWidget(exit_button)
        
        exit_button.clicked.connect(self.controller.exit_app)
        
        # Align buttons to the top
        self.sidebar_layout.setAlignment(Qt.AlignmentFlag.AlignTop)