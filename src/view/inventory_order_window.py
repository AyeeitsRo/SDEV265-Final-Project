# --- Standard PyQt6 imports for UI widgets, layouts, styling, and core functionality ---
from PyQt6.QtWidgets import (
    QFrame, QVBoxLayout, QWidget, QLabel,
    QHBoxLayout, QApplication, QPushButton, QLineEdit,
    QScrollArea, QMessageBox, QTableWidget, QTableWidgetItem
)
from PyQt6.QtGui import QFont, QColor
from PyQt6.QtCore import Qt
import re

# Import sidebar and mock incoming order data
from sidebar import *
from model.incoming_orders import orders

# Main class for the Inventory Order Window
class InventoryOrderWindow(QWidget):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.setWindowTitle("Inventory Ordering")
        self.resize(1700, 1000)

        # Center window on screen
        screen = QApplication.primaryScreen()
        screen_geometry = screen.availableGeometry()
        x = (screen_geometry.width() - self.width()) // 2
        y = (screen_geometry.height() - self.height()) // 2
        self.setGeometry(x, y, self.width(), self.height())

        self.setStyleSheet('background-color: #FAF9F6;')  # Light background

        self.entry_count = 0  # Track number of SKU entries

        # Top-level layout: horizontal split between sidebar and content
        main_layout = QHBoxLayout()
        self.setLayout(main_layout)

        # --- Sidebar Setup ---
        window_names = ['Home', 'Order Material', 'Inventory', 'Outgoing Work Orders']
        sidebar_frame = QFrame()
        sidebar_frame.setFixedWidth(200)

        frame_layout = QVBoxLayout()
        frame_layout.setContentsMargins(0, 0, 0, 0)
        frame_layout.setSpacing(0)

        sidebar = Sidebar(window_names, self.controller)
        frame_layout.addWidget(sidebar)
        sidebar_frame.setLayout(frame_layout)
        main_layout.addWidget(sidebar_frame)

        # --- Main Content Layout ---
        content_layout = QVBoxLayout()
        main_layout.addLayout(content_layout)

        # Page Title
        self.label = QLabel("Order Material")
        self.label.setFont(QFont("Roboto", 32))
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setStyleSheet('color: #228B22;')
        content_layout.addWidget(self.label)

        # Container to hold both the order table and entry section
        scroll_split_container = QWidget()
        scroll_split_layout = QVBoxLayout(scroll_split_container)
        scroll_split_layout.setContentsMargins(0, 0, 0, 0)
        scroll_split_layout.setSpacing(20)

        # --- Order Table Section ---
        order_table_widget = QWidget()
        order_table_layout = QVBoxLayout(order_table_widget)
        order_table_layout.setContentsMargins(0, 0, 0, 0)

        self.order_table = QTableWidget()
        self.order_table.setColumnCount(4)
        self.order_table.setHorizontalHeaderLabels([
            "Order ID", "Expected Arrival", "Shipping Status", "# of Items"
        ])

        # Column width and appearance
        self.order_table.horizontalHeader().setStretchLastSection(False)
        self.order_table.setColumnWidth(0, 350)
        self.order_table.setColumnWidth(1, 350)
        self.order_table.setColumnWidth(2, 350)
        self.order_table.setColumnWidth(3, 350)

        self.order_table.setStyleSheet("""
            QHeaderView::section {
                background-color: #228B22;
                color: black;
                padding: 6px;
                font-family: Roboto;
                font-size: 9pt;
                font-weight: bold;
            }
            QTableWidget {
                alternate-background-color: #f0f0f0;
                background-color: white;
            }
        """)
        self.order_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)

        # Fill the order table with data from the model
        self.order_table.setRowCount(len(orders))
        font = QFont("Roboto", 10)
        for row_index, order in enumerate(orders):
            for col_index, value in enumerate([order["id"], order["arrival"], order["status"], str(order["items"])]):
                item = QTableWidgetItem(value)
                item.setForeground(QColor('black'))
                item.setFont(font)
                self.order_table.setItem(row_index, col_index, item)

        self.order_table.setAlternatingRowColors(True)
        order_table_layout.addWidget(self.order_table)

        # Wrap table in a scroll area
        order_scroll = QScrollArea()
        order_scroll.setWidgetResizable(True)
        order_scroll.setWidget(order_table_widget)
        order_scroll.setFixedHeight(200)
        scroll_split_layout.addWidget(order_scroll)

        # --- "+ Add" Button (Below Table) ---
        add_button_layout = QHBoxLayout()
        add_button_layout.addStretch()
        self.add_button = QPushButton("+")
        self.add_button.setFixedSize(50, 50)
        self.add_button.clicked.connect(self.add_entry)
        self.add_button.setStyleSheet("""
            background-color: #228B22;
            color: white;
            font-size: 30px;
            font: bold;
            border-radius: 8px;
            border: none;
        """)
        add_button_layout.addWidget(self.add_button)
        scroll_split_layout.addLayout(add_button_layout)

        # --- Scrollable Entry Form Section ---
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)

        self.scroll_content = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_content)
        self.scroll_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.scroll_area.setWidget(self.scroll_content)
        self.scroll_area.setMinimumHeight(400)
        scroll_split_layout.addWidget(self.scroll_area)

        # Add container to main layout
        content_layout.addWidget(scroll_split_container)

        # --- Submit Button at Bottom Right ---
        submit_container = QWidget()
        submit_layout = QHBoxLayout(submit_container)
        submit_layout.setContentsMargins(0, 10, 10, 10)
        submit_layout.addStretch()

        submit_button = QPushButton("Submit")
        submit_button.clicked.connect(lambda: self.controller.handle_submit(self))
        submit_button.setFixedSize(120, 40)
        submit_button.setStyleSheet("""
            background-color: #228B22;
            color: white;
            font-size: 16px;
            border-radius: 8px;
        """)
        submit_layout.addWidget(submit_button)
        content_layout.addWidget(submit_container)

        # Add first entry row by default
        self.add_entry()

    # --- Dynamically Add Entry Fields ---
    def add_entry(self):
        self.entry_count += 1
        entry_frame = QFrame()

        # Alternate background for every other entry
        if self.entry_count % 2 == 0:
            entry_frame.setStyleSheet("background-color: #F0F0F0; border: 1px solid #CCCCCC; border-radius: 8px;")
        else:
            entry_frame.setStyleSheet("background-color: transparent;")

        entry_layout = QVBoxLayout(entry_frame)
        entry_layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        entry_layout.setSpacing(10)

        # SKU Input Row
        sku_row = QHBoxLayout()
        sku_label = QLabel("SKU:")
        sku_label.setFont(QFont("Roboto", 10, QFont.Weight.Bold))
        sku_label.setStyleSheet("color: black;")

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
        sku_row.addStretch()

        # Quantity Input Row
        quantity_row = QHBoxLayout()
        quantity_label = QLabel("Quantity:")
        quantity_label.setFont(QFont("Roboto", 10, QFont.Weight.Bold))
        quantity_label.setStyleSheet("color: black;")

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
        quantity_row.addStretch()

        # Add "-" remove button for all entries after the first one
        if self.entry_count > 1:
            remove_button = QPushButton("-")
            remove_button.setFixedSize(30, 30)
            remove_button.setStyleSheet("""
                background-color: red;
                color: white;
                font-size: 16px;
                font: bold;
                border-radius: 15px;
                border: none;
            """)
            remove_button.clicked.connect(lambda: self.remove_entry(entry_frame))

            remove_button_layout = QHBoxLayout()
            remove_button_layout.addStretch()
            remove_button_layout.addWidget(remove_button)
            entry_layout.addLayout(remove_button_layout)

        # Add SKU and Quantity rows to the entry
        entry_layout.addLayout(sku_row)
        entry_layout.addLayout(quantity_row)
        self.scroll_layout.addWidget(entry_frame)

    # Remove a SKU entry section
    def remove_entry(self, entry_frame):
        self.scroll_layout.removeWidget(entry_frame)
        entry_frame.deleteLater()

    # Live validate SKU format
    def validate_sku(self, text, input_box):
        pattern = r"^[A-Z]{3}-\d{4}$"
        if text and not re.fullmatch(pattern, text):
            input_box.setStyleSheet("""
                background-color: #E0E0E0;
                border: 2px solid red;
                border-radius: 4px;
                padding: 5px;
                color: black;
            """)
        else:
            input_box.setStyleSheet("""
                background-color: #E0E0E0;
                border: 2px solid #228B22;
                border-radius: 4px;
                padding: 5px;
                color: black;
            """)

    # Live validate quantity is numeric
    def validate_quantity(self, text, input_box):
        if text and not text.isdigit():
            input_box.setStyleSheet("""
                background-color: #E0E0E0;
                border: 2px solid red;
                border-radius: 4px;
                padding: 5px;
                color: black;
            """)
        else:
            input_box.setStyleSheet("""
                background-color: #E0E0E0;
                border: 2px solid #228B22;
                border-radius: 4px;
                padding: 5px;
                color: black;
            """)
