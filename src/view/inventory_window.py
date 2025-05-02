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
    Inventory (Search) Window using same layout as OrderWindow
    '''
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.setWindowTitle("Inventory System")
        self.resize(1700, 1000)

        # Center window
        screen = QApplication.primaryScreen()
        screen_geometry = screen.availableGeometry()
        x = (screen_geometry.width() - self.width()) // 2
        y = (screen_geometry.height() - self.height()) // 2
        self.setGeometry(x, y, self.width(), self.height())

        self.setStyleSheet('background-color: #FAF9F6;')
        self.inventory_data = inventory_data

        # Layouts
        main_layout = QHBoxLayout()
        self.setLayout(main_layout)

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

        content_layout = QVBoxLayout()
        main_layout.addLayout(content_layout)

        # Header
        self.label = QLabel("Inventory")
        self.label.setFont(QFont("Roboto", 32))
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setStyleSheet('color: #228B22;')
        content_layout.addWidget(self.label)

        # Search Bar
        self.search_layout = QHBoxLayout()

        # Search box
        self.search_box = QLineEdit(self)
        self.search_box.setPlaceholderText("Search inventory...")
        self.search_box.setFixedWidth(400)  # Set width to 1/4 of the screen
        self.search_box.setStyleSheet("""
            border: 2px solid #228B22;
            border-radius: 4px;
            padding: 5px;
            color: black;
        """)
        self.search_box.textChanged.connect(self.on_search)

        # Search button
        self.clear_button = QPushButton("Clear Search", self)
        self.clear_button.setFixedWidth(125) 
        self.clear_button.clicked.connect(self.clear_search)
        self.clear_button.setStyleSheet("""
            background-color: #228B22;
            color: white;
            border-radius: 4px;
            padding: 5px;
        """)

        self.search_layout.addWidget(self.search_box)
        self.search_layout.addWidget(self.clear_button)

        # Adjust alignment
        self.search_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        content_layout.addLayout(self.search_layout)

        # Table
        self.inventory_table = QTableWidget()
        self.inventory_table.setColumnCount(6)
        self.inventory_table.setHorizontalHeaderLabels(["#", "Item Name", "Description", "SKU", "Price", "Quantity"])
        
        header = self.inventory_table.horizontalHeader()
        font = QFont("Roboto", 11)
        font.setItalic(True)
        font.setBold(False)
        header.setFont(font)

        self.inventory_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.inventory_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.inventory_table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.inventory_table.verticalHeader().setVisible(False)
        self.inventory_table.horizontalHeader().setStretchLastSection(True)
        self.inventory_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

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

        content_layout.addWidget(self.inventory_table)

        self.populate_inventory()

    def populate_inventory(self):
        """Populates the inventory in the table"""
        self.inventory_table.setRowCount(len(self.inventory_data))

        for row, item_data in enumerate(self.inventory_data):
            number_item = QTableWidgetItem(str(row + 1))
            number_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self._style_item(number_item)
            self.inventory_table.setItem(row, 0, number_item)

            for col, value in enumerate(item_data, start=1):
                item = QTableWidgetItem(str(value))
                self._style_item(item)
                self.inventory_table.setItem(row, col, item)


    def on_search(self):
        """Handles search action when the button is clicked."""
        query = self.search_box.text()  # Get the text from the search box
        filtered_data = search_inventory(query, self.inventory_data)  # Call the search function
        self.populate_filtered_inventory(filtered_data)

    def populate_filtered_inventory(self, filtered_data):
        """Populate the table with filtered data."""
        self.inventory_table.setRowCount(len(filtered_data))

        for row, item_data in enumerate(filtered_data):
            # Column 0: Row number
            number_item = QTableWidgetItem(str(row + 1))
            number_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self._style_item(number_item)
            self.inventory_table.setItem(row, 0, number_item)

            # Columns 1–5: Item Name, Description, SKU, Price, Quantity
            for col, value in enumerate(item_data, start=1):
                if col == 4:  # Price column (index 3 in data)
                    formatted_price = f"${value:.2f}"
                    item = QTableWidgetItem(formatted_price)
                else:
                    item = QTableWidgetItem(str(value))
                self._style_item(item)
                self.inventory_table.setItem(row, col, item)


    def _style_item(self, item):
        """Helper to apply consistent styling to table items"""
        item.setForeground(Qt.GlobalColor.darkGreen)
        font = item.font()
        font.setPointSize(10)
        font.setBold(True)
        item.setFont(font)
        
    def clear_search(self):
        """Clear the search box and reset the table data."""
        self.search_box.clear() 
        self.populate_inventory()  
