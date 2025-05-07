from PyQt6.QtWidgets import (
    QFrame, QVBoxLayout, QWidget, QLabel, QHeaderView,
    QHBoxLayout, QApplication, QTableWidget, QTableWidgetItem,
    QLineEdit, QPushButton
)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt

from sidebar import *  
from model.inventory import *  
from model.inventory_data import * 


class InventoryWindow(QWidget):
    '''
    Inventory (Search) Window using same layout style as the OrderWindow.
    Displays inventory items with a search bar and sidebar navigation.
    '''
    def __init__(self, controller):
        super().__init__()

        self.controller = controller  # Main app controller for routing
        self.setWindowTitle("Inventory System")
        self.resize(1700, 1000)

        # === Center the window on screen ===
        screen = QApplication.primaryScreen()
        screen_geometry = screen.availableGeometry()
        x = (screen_geometry.width() - self.width()) // 2
        y = (screen_geometry.height() - self.height()) // 2
        self.setGeometry(x, y, self.width(), self.height())

        # Set background color
        self.setStyleSheet('background-color: #FAF9F6;')

        self.inventory_data = inventory_data  # Load dataset from model

        # === Main Layouts ===
        main_layout = QHBoxLayout()  # Horizontal layout to hold sidebar + content
        self.setLayout(main_layout)

        # === Sidebar ===
        window_names = ['Home', 'Order Material', 'Inventory', 'Outgoing Work Orders']
        sidebar_frame = QFrame()
        sidebar_frame.setFixedWidth(200)  # Sidebar width

        frame_layout = QVBoxLayout()
        frame_layout.setContentsMargins(0, 0, 0, 0)
        frame_layout.setSpacing(0)

        sidebar = Sidebar(window_names, self.controller)  # Create Sidebar widget
        frame_layout.addWidget(sidebar)
        sidebar_frame.setLayout(frame_layout)
        main_layout.addWidget(sidebar_frame)

        # === Content Area ===
        content_layout = QVBoxLayout()
        main_layout.addLayout(content_layout)

        # === Title Header ===
        self.label = QLabel("Inventory")
        self.label.setFont(QFont("Roboto", 32))
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setStyleSheet('color: #228B22;')
        content_layout.addWidget(self.label)

        # === Search Bar ===
        self.search_layout = QHBoxLayout()

        # Search input box
        self.search_box = QLineEdit(self)
        self.search_box.setPlaceholderText("Search inventory...")
        self.search_box.setFixedWidth(400)
        self.search_box.setStyleSheet("""
            border: 2px solid #228B22;
            border-radius: 4px;
            padding: 5px;
            color: black;
        """)
        self.search_box.textChanged.connect(self.on_search)

        # Clear button
        self.clear_button = QPushButton("Clear Search", self)
        self.clear_button.setFixedWidth(125)
        self.clear_button.clicked.connect(self.clear_search)
        self.clear_button.setStyleSheet("""
            background-color: #228B22;
            color: white;
            border-radius: 4px;
            padding: 5px;
        """)

        # Add search box and button to layout
        self.search_layout.addWidget(self.search_box)
        self.search_layout.addWidget(self.clear_button)
        self.search_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)

        content_layout.addLayout(self.search_layout)

        # === Inventory Table ===
        self.inventory_table = QTableWidget()
        self.inventory_table.setColumnCount(6)  # 6 columns total
        self.inventory_table.setHorizontalHeaderLabels([
            "#", "Item Name", "Description", "SKU", "Price", "Quantity"
        ])

        # Header style
        header = self.inventory_table.horizontalHeader()
        font = QFont("Roboto", 11)
        font.setItalic(True)
        font.setBold(False)
        header.setFont(font)

        # Table behavior
        self.inventory_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.inventory_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.inventory_table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.inventory_table.verticalHeader().setVisible(False)
        self.inventory_table.horizontalHeader().setStretchLastSection(True)
        self.inventory_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        # Row styling
        self.inventory_table.setAlternatingRowColors(True)
        self.inventory_table.setStyleSheet("""
            QTableWidget {
                alternate-background-color: #f0f0f0;
                background-color: white;
            }
            QHeaderView::section {
                background-color: #228B22;
                color: black;
                font-weight: italic;
                font-size: 11pt;
                font-family: Roboto;
                padding: 4px;
            }
        """)

        # Add table to content layout
        content_layout.addWidget(self.inventory_table)

        # Populate table with data
        self.populate_inventory()

    def populate_inventory(self):
        """Fill the table with all inventory items."""
        self.inventory_table.setRowCount(len(self.inventory_data))

        for row, item_data in enumerate(self.inventory_data):
            # Row number (column 0)
            number_item = QTableWidgetItem(str(row + 1))
            number_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self._style_item(number_item)
            self.inventory_table.setItem(row, 0, number_item)

            # Data columns (columns 1–5)
            for col, value in enumerate(item_data, start=1):
                item = QTableWidgetItem(str(value))
                self._style_item(item)
                self.inventory_table.setItem(row, col, item)

    def on_search(self):
        """Trigger search filtering as user types."""
        query = self.search_box.text()  # Get input
        filtered_data = search_inventory(query, self.inventory_data)  # Search logic from model
        self.populate_filtered_inventory(filtered_data)

    def populate_filtered_inventory(self, filtered_data):
        """Display only filtered search results in table."""
        self.inventory_table.setRowCount(len(filtered_data))

        for row, item_data in enumerate(filtered_data):
            # Row number
            number_item = QTableWidgetItem(str(row + 1))
            number_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self._style_item(number_item)
            self.inventory_table.setItem(row, 0, number_item)

            # Item columns
            for col, value in enumerate(item_data, start=1):
                if col == 4:  # Price column — format as currency
                    formatted_price = f"${value:.2f}"
                    item = QTableWidgetItem(formatted_price)
                else:
                    item = QTableWidgetItem(str(value))
                self._style_item(item)
                self.inventory_table.setItem(row, col, item)

    def _style_item(self, item):
        """Style table cell item with consistent font and color."""
        item.setForeground(Qt.GlobalColor.darkGreen)
        font = item.font()
        font.setPointSize(10)
        font.setBold(True)
        item.setFont(font)

    def clear_search(self):
        """Clear the search bar and repopulate full inventory list."""
        self.search_box.clear()
        self.populate_inventory()
