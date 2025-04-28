from PyQt6.QtWidgets import (
    QFrame, QVBoxLayout, QWidget, QLabel, 
    QHBoxLayout, QApplication, QPushButton, QLineEdit,
    QScrollArea, QMessageBox
)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt
import re

from sidebar import *

class InventoryOrderWindow(QWidget):
    '''
    The main window of the inventory system.
    '''
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.setWindowTitle("Inventory System")
        self.resize(1700, 1000)

        # Center the window
        screen = QApplication.primaryScreen()
        screen_geometry = screen.availableGeometry()
        x = (screen_geometry.width() - self.width()) // 2
        y = (screen_geometry.height() - self.height()) // 2
        self.setGeometry(x, y, self.width(), self.height())

        # Set background color
        self.setStyleSheet('background-color: #FAF9F6;')

        # Main Layout
        main_layout = QHBoxLayout()
        self.setLayout(main_layout)

        # Sidebar
        window_names = ['Home', 'Order Material', 'Inventory', 'Outgoing Work Orders']
        sidebar_frame = QFrame()
        sidebar_frame.setFixedWidth(200)

        frame_layout = QVBoxLayout()
        frame_layout.setContentsMargins(0, 0, 0, 0)
        frame_layout.setSpacing(0)

        sidebar = Sidebar(window_names, self.controller)
        frame_layout.addWidget(sidebar)
        sidebar_frame.setLayout(frame_layout)

        # Add sidebar to the main layout
        main_layout.addWidget(sidebar_frame)

        # Main content layout (the space next to the sidebar)
        content_layout = QVBoxLayout()
        main_layout.addLayout(content_layout)

        # Top label
        self.label = QLabel("Order Material")
        self.label.setFont(QFont("Roboto", 32))
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setStyleSheet('color: #228B22;')
        content_layout.addWidget(self.label)

        # Top bar for "+" button
        top_bar = QHBoxLayout()
        top_bar.addStretch()

        self.add_button = QPushButton("+")
        self.add_button.setFixedSize(40, 40)
        self.add_button.clicked.connect(self.add_entry)
        self.add_button.setStyleSheet("""
            background-color: #228B22;
            color: white;
            font-size: 20px;
            border-radius: 20px;
        """)
        top_bar.addWidget(self.add_button)
        content_layout.addLayout(top_bar)

        # Scroll Area
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)

        self.scroll_content = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_content)
        self.scroll_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.scroll_area.setWidget(self.scroll_content)
        content_layout.addWidget(self.scroll_area)

        # Add the first input row
        self.add_entry()

    def add_entry(self):
        entry_frame = QFrame()
        entry_layout = QVBoxLayout(entry_frame)
        entry_layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        entry_layout.setSpacing(10)

        # --- SKU Row ---
        sku_row = QHBoxLayout()
        sku_row.setAlignment(Qt.AlignmentFlag.AlignLeft)

        sku_label = QLabel("SKU:")
        sku_label.setFont(QFont("Roboto", 10, QFont.Weight.Bold))
        sku_label.setStyleSheet("color: black;")  # Make label text black

        sku_input = QLineEdit()
        sku_input.setPlaceholderText("ABC-1234")
        sku_input.setFixedWidth(200)
        sku_input.setMaxLength(8)
        sku_input.setStyleSheet("""
            background-color: #E0E0E0;
            border: 2px solid #228B22;
            border-radius: 4px;
            padding: 5px;
            color: black;
        """)
        sku_input.textChanged.connect(lambda text: self.validate_sku(text, sku_input))

        sku_row.addWidget(sku_label)
        sku_row.addWidget(sku_input)

        # --- Quantity Row ---
        quantity_row = QHBoxLayout()
        quantity_row.setAlignment(Qt.AlignmentFlag.AlignLeft)

        quantity_label = QLabel("Quantity:")
        quantity_label.setFont(QFont("Roboto", 10, QFont.Weight.Bold))
        quantity_label.setStyleSheet("color: black;")  # Make label text black

        quantity_input = QLineEdit()
        quantity_input.setPlaceholderText("Enter Quantity")
        quantity_input.setFixedWidth(200)
        quantity_input.setMaxLength(5)
        quantity_input.setStyleSheet("""
            background-color: #E0E0E0;
            border: 2px solid #228B22;
            border-radius: 4px;
            padding: 5px;
            color: black;
        """)
        quantity_input.textChanged.connect(lambda text: self.validate_quantity(text, quantity_input))

        quantity_row.addWidget(quantity_label)
        quantity_row.addWidget(quantity_input)

        # Add both rows to the entry layout
        entry_layout.addLayout(sku_row)
        entry_layout.addLayout(quantity_row)

        # Add the entry frame to the scroll layout
        self.scroll_layout.addWidget(entry_frame)

    def validate_sku(self, text, input_box):
        """ Validate SKU format (XXX-XXXX). """
        pattern = r"^[A-Z]{3}-\d{4}$"
        if not re.match(pattern, text) and text != "":
            input_box.setStyleSheet("border: 2px solid red;")
        else:
            input_box.setStyleSheet("""
                background-color: #E0E0E0;
                border: 2px solid #228B22;
                border-radius: 4px;
                padding: 5px;
                color: black;
            """)

    def validate_quantity(self, text, input_box):
        """ Validate quantity to be digits only and warn if 100+. """
        if not text.isdigit() and text != "":
            input_box.setStyleSheet("border: 2px solid red;")
        else:
            input_box.setStyleSheet("""
                background-color: #E0E0E0;
                border: 2px solid #228B22;
                border-radius: 4px;
                padding: 5px;
                color: black;
            """)

            if text.isdigit() and int(text) >= 100:
                reply = QMessageBox.question(
                    self, "Confirm Quantity",
                    f"Are you sure you want to order {text} units?",
                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
                )
                if reply == QMessageBox.StandardButton.No:
                    input_box.clear()
