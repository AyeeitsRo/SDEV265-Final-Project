from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

from controller.controller import Controller

class Sidebar(QWidget):
    def __init__(self, window_names, parent=None):
        super().__init__(parent)

        # Create layout for sidebar 
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.setFixedWidth(180)
        
        # Create buttons for each window name
        for window_name in window_names:
            button = QPushButton(window_name)
            # Button styling (off-white background and black text)
            button.setStyleSheet("background-color: #228B22; color: black;") # Sets background color of buttons to green and button text to black
            button.setFixedHeight(40) # Set a fixed height for each button
            button.setFixedWidth(170)
            button.setFont(QFont('Roboto', 12))
            self.layout.addWidget(button)
            
        self.layout.addStretch()
        
        # Create Exit button on bottom of sidebar
        exit_button = QPushButton("Exit")
        exit_button.setStyleSheet("background-color: #228B22; color: black;")
        exit_button.setFixedHeight(40)
        exit_button.setFixedWidth(170)
        exit_button.setFont(QFont('Roboto', 12))
        self.layout.addWidget(exit_button)
        
        exit_button.clicked.connect(Controller.exit_app)
        
        # Align buttons to the top
        self.layout.setAlignment(Qt.AlignmentFlag.AlignTop)