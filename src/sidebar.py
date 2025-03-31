from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton
from PyQt6.QtCore import Qt

class Sidebar(QWidget):
    def __init__(self, window_names, parent=None):
        super().__init__(parent)

        # Create layout for sidebar (QVBoxLayout)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Set the background color of the sidebar (forest green)
        self.setStyleSheet("background-color: #228B22;")
        
        # Create buttons for each window name
        for window_name in window_names:
            button = QPushButton(window_name)
            # Button styling (off-white background and black text)
            button.setStyleSheet("""
                background-color: #228B22;
                color: black;
                padding: 5px;
                margin: 3px;
            """)
            button.setFixedHeight(50) # Set a fixed height for each button
            button.setFixedWidth(200)
            self.layout.addWidget(button)
            
        # Align buttons to the top
        self.layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        

        