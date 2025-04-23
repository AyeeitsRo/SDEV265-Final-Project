
from PyQt6.QtWidgets import (
    QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel, 
    QHBoxLayout, QListWidget, QListWidgetItem, QMessageBox, QApplication
)
from PyQt6.QtGui import QFont, QPixmap
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QScreen

from sidebar import *


class SearchWindow(QWidget):
    '''
    The main window of the inventory system.
    '''
    def __init__(self, controller):
        """
        Initalizes the MainWindow

        Args:
            controller (Controller): The application's main controller.
        """
        super().__init__()
        self.controller = controller
        self.setWindowTitle("Inventory System") # Sets title of window
        self.resize(1700, 1000) # Sets window size
        
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
        
        # Main Layout
        main_layout = QHBoxLayout()
        self.setLayout(main_layout)
        
        # Sidebar (navigation bar)       
        window_names = ['Home', 'Order Material', 'Inventory', 'Outgoing Work Orders',]
        sidebar = Sidebar(window_names, self.controller)
        main_layout.addWidget(sidebar)
        
        # Main content layout (label)
        content_layout = QVBoxLayout()  # Create a vertical layout for the content
        main_layout.addLayout(content_layout)  # Add the content layout to the main layout
        
        # Add main label overhead
        self.label = QLabel("") # Sets the text inside the label
        self.label.setFont(QFont("Roboto", 32)) # Sets label in "roboto" style with a 32 point font
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter) # Centers the label
        self.label.setStyleSheet('color: #228B22;') # Sets label text color to dark green
        main_layout.addWidget(self.label)


    # MAYBE A LOW INVENTORY ALERT BOX!