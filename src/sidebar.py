from typing import List, Optional, Any

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QSizePolicy, QLabel
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QPixmap


class Sidebar(QWidget):
    """
    Sidebar widget that displays navigation buttons and a logo image on the left side of the main window.

    This sidebar includes:
    - Navigation buttons based on window names.
    - A company logo image.
    - An 'Exit' button to close the application.

    Each navigation button is connected to the corresponding method in the controller.
    """

    def __init__(self, window_names: List[str], controller: Any, parent: Optional[QWidget] = None) -> None:
        """
        Initializes the Sidebar widget.

        Args:
            window_names (List[str]): List of window names to create buttons for.
            controller (Any): Controller object that contains methods to open different windows.
            parent (Optional[QWidget]): Parent widget, if any.
        """
        super().__init__(parent)

        self.controller = controller  # Reference to the app's controller, used to connect button actions

        # Create vertical layout for all sidebar widgets
        self.sidebar_layout = QVBoxLayout()  # Main vertical layout for sidebar
        self.setLayout(self.sidebar_layout)  # Set layout to this widget
        self.setFixedWidth(180)  # Set fixed width for the sidebar
        self.sidebar_layout.setContentsMargins(0, 0, 0, 0)  # Remove margins around layout
        self.sidebar_layout.setSpacing(0)  # Remove spacing between widgets

        # === Create navigation buttons ===
        for window_name in window_names:
            button = QPushButton(window_name)  # Create a button with the window name
            button.setStyleSheet("background-color: #228B22; color: black;")  # Set button style
            button.setFixedHeight(40)  # Set fixed height
            button.setFixedWidth(170)  # Set fixed width
            button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)  # Expand horizontally if needed
            button.setFont(QFont('Roboto', 12))  # Set font style and size
            self.sidebar_layout.addWidget(button)  # Add button to sidebar layout

            # Connect button to the appropriate controller method
            if window_name == "Outgoing Work Orders":
                button.clicked.connect(self.controller.open_order)  # Open the order window
            elif window_name == "Order Material":
                button.clicked.connect(self.controller.open_search)  # Open the material search window
            elif window_name == "Inventory":
                button.clicked.connect(self.controller.open_inventory)  # Open inventory window
            elif window_name == "Home":
                button.clicked.connect(self.controller.open_home)  # Return to home dashboard

        # Add stretch to push remaining widgets to the bottom
        self.sidebar_layout.addStretch()  # Flexible spacer pushing the logo and exit button to the bottom

        # === Company Logo Section ===
        image_label = QLabel()  # QLabel to hold the company logo
        pixmap = QPixmap("resources/company-logo.png")  # Load image from file
        pixmap = pixmap.scaled(120, 120, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)  # Scale the image while keeping aspect ratio
        image_label.setPixmap(pixmap)  # Set the pixmap into the label
        image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Center-align the image
        self.sidebar_layout.addWidget(image_label)  # Add logo to the layout

        # === Exit Button Section ===
        exit_button = QPushButton("Exit")  # Create 'Exit' button
        exit_button.setStyleSheet("background-color: #228B22; color: black;")  # Set button style
        exit_button.setFixedHeight(40)  # Set height
        exit_button.setFixedWidth(170)  # Set width
        exit_button.setFont(QFont('Roboto', 12))  # Set font style and size
        self.sidebar_layout.addWidget(exit_button)  # Add exit button to layout

        exit_button.clicked.connect(self.controller.exit_app)  # Connect to app exit method in controller

        self.sidebar_layout.setAlignment(Qt.AlignmentFlag.AlignTop)  # Align all items to the top of the sidebar
