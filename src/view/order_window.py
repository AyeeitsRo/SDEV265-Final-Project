from PyQt6.QtWidgets import (
    QFrame, QVBoxLayout, QWidget, QLabel, QHeaderView,
    QHBoxLayout, QApplication, QTableWidget, QTableWidgetItem,
    QComboBox, QLineEdit, QPushButton
)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt

from sidebar import *
from model.order import OrderManager
from typing import List


class OrderWindow(QWidget):
    '''
    The main window for managing work orders in the inventory system.
    Displays a sidebar for navigation, a searchable table of orders,
    and options to modify order status.
    '''
    def __init__(self, controller) -> None:
        """
        Initializes the OrderWindow interface.

        Args:
            controller: The main controller handling navigation and events.
        """
        super().__init__()
        self.controller = controller  # Reference to the main application controller

        self.setWindowTitle("Inventory System")  # Set the window title
        self.resize(1700, 1000)  # Set the default window size

        self.order_manager: OrderManager = OrderManager()  # Manager handling all order-related logic
        self.order_manager.seed_orders()  # Populate with initial order data

        screen = QApplication.primaryScreen()  # Get the primary screen object
        screen_geometry = screen.availableGeometry()  # Get the available screen geometry
        x = (screen_geometry.width() - self.width()) // 2  # Calculate horizontal center
        y = (screen_geometry.height() - self.height()) // 2  # Calculate vertical center
        self.setGeometry(x, y, self.width(), self.height())  # Center the window on screen

        self.setStyleSheet('background-color: #FAF9F6;')  # Set background color

        main_layout = QHBoxLayout()  # Main horizontal layout
        self.setLayout(main_layout)

        window_names: List[str] = ['Home', 'Order Material', 'Inventory', 'Outgoing Work Orders']  # Sidebar tab names

        sidebar_frame = QFrame()  # Frame to contain the sidebar
        sidebar_frame.setFixedWidth(200)  # Set fixed width for sidebar frame

        frame_layout = QVBoxLayout()  # Layout for the sidebar frame
        frame_layout.setContentsMargins(0, 0, 0, 0)  # Remove margins
        frame_layout.setSpacing(0)  # Remove spacing

        sidebar = Sidebar(window_names, self.controller)  # Sidebar widget for navigation
        frame_layout.addWidget(sidebar)  # Add sidebar to layout
        sidebar_frame.setLayout(frame_layout)  # Apply layout to sidebar frame

        main_layout.addWidget(sidebar_frame)  # Add sidebar frame to main layout

        content_layout = QVBoxLayout()  # Layout for the main content area
        main_layout.addLayout(content_layout)

        self.label = QLabel("Work Orders")  # Main heading label
        self.label.setFont(QFont("Roboto", 32))  # Set label font
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Center the text
        self.label.setStyleSheet('color: #228B22;')  # Set text color
        content_layout.addWidget(self.label)  # Add label to content layout

        self.search_layout = QHBoxLayout()  # Layout for the search bar section

        self.search_box = QLineEdit(self)  # Input field for searching orders
        self.search_box.setPlaceholderText("Search work orders...")  # Set placeholder
        self.search_box.setFixedWidth(400)  # Set fixed width
        self.search_box.setStyleSheet("""
            border: 2px solid #228B22;
            border-radius: 4px;
            padding: 5px;
            color: black;
        """)
        self.search_box.textChanged.connect(self.on_search)  # Connect text change to filter logic

        self.clear_button = QPushButton("Clear Search", self)  # Button to clear search field
        self.clear_button.setFixedWidth(125)  # Set fixed width
        self.clear_button.setStyleSheet("""
            background-color: #228B22;
            color: white;
            border-radius: 4px;
            padding: 5px;
        """)
        self.clear_button.clicked.connect(self.clear_search)  # Connect button to clear action

        self.search_layout.addWidget(self.search_box)  # Add search box to layout
        self.search_layout.addWidget(self.clear_button)  # Add clear button to layout
        self.search_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)  # Align left

        content_layout.addLayout(self.search_layout)  # Add search layout to content

        self.order_table = QTableWidget()  # Table to display order data
        self.order_table.setColumnCount(5)  # Set number of columns
        self.order_table.setHorizontalHeaderLabels(["Order ID", "Date", "Shipping", "Price", "Status"])  # Set headers
        self.order_table.setStyleSheet("""
            QHeaderView::section {
                background-color: #228B22;
                color: black;
                font-weight: italic;
                font-size: 11pt;
                font-family: Roboto;
                padding: 4px;
            }
            QTableWidget {
                alternate-background-color: #f0f0f0;
                background-color: white;
            }
        """)
        self.order_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)  # Disable editing
        self.order_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)  # Select entire rows
        self.order_table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)  # Only allow single row selection
        self.order_table.verticalHeader().setVisible(False)  # Hide row numbers
        self.order_table.horizontalHeader().setStretchLastSection(True)  # Stretch last column
        self.order_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)  # Stretch columns evenly
        content_layout.addWidget(self.order_table)  # Add table to layout

        self.populate_orders()  # Fill table with data


    def populate_orders(self) -> None:
        """
        Populates the order table with all available orders.
        """
        self.populate_filtered_orders(self.order_manager.get_orders())


    def populate_filtered_orders(self, orders) -> None:
        """
        Populates the order table with a filtered list of orders.

        Args:
            orders (List[Order]): The list of order objects to display.
        """
        self.order_table.setRowCount(0)  # Clear existing rows
        self.order_table.setRowCount(len(orders))  # Set new row count

        for row, order in enumerate(orders):
            data = [order.order_id, order.date, order.shipping_type, f"${order.price:.2f}"]  # Order details

            for col, value in enumerate(data):
                item = QTableWidgetItem(str(value))  # Create table cell item
                item.setForeground(Qt.GlobalColor.darkGreen)  # Set text color
                font = item.font()  # Get font object
                font.setPointSize(10)  # Set font size
                font.setBold(True)  # Set font bold
                item.setFont(font)  # Apply font
                self.order_table.setItem(row, col, item)  # Set item in table

            combo = QComboBox()  # Dropdown for order status
            combo.addItems(["Pending", "Processing", "Shipped", "Delivered"])  # Status options
            combo.setCurrentText(order.status)  # Set current status
            combo.setStyleSheet("""
                QComboBox {
                    background-color: white;
                    color: black;
                    font-size: 10pt;
                }
                QComboBox::drop-down {
                    background-color: #228B22;
                }
                QComboBox QAbstractItemView {
                    background-color: white;
                    color: black;
                    selection-background-color: #228B22;
                    selection-color: white;
                }
            """)
            combo.currentTextChanged.connect(lambda new_status, row=row: self.change_order_status(row, new_status))  # Connect to change handler
            self.order_table.setCellWidget(row, 4, combo)  # Add combo box to table


    def change_order_status(self, row: int, new_status: str) -> None:
        """
        Updates the status of the selected order.

        Args:
            row (int): The row number of the order in the table.
            new_status (str): The new status to apply.
        """
        order_id = self.order_table.item(row, 0).text()  # Get order ID from table
        order = self.order_manager.get_order_by_id(order_id)  # Retrieve order object

        if order and order.status != new_status:
            order.change_status(new_status)  # Update status
            self.populate_orders()  # Refresh table


    def on_search(self) -> None:
        """
        Filters the displayed orders based on the search query.
        """
        query = self.search_box.text().lower()  # Get lowercase search query
        filtered_orders = []  # List to hold matched orders

        for order in self.order_manager.get_orders():
            row_data = [
                str(order.order_id),
                str(order.date),
                str(order.shipping_type),
                f"${order.price:.2f}",
                str(order.status)
            ]
            if any(query in field.lower() for field in row_data):
                filtered_orders.append(order)  # Add matching order

        self.populate_filtered_orders(filtered_orders)  # Display matched orders


    def clear_search(self) -> None:
        """
        Clears the search box and resets the order table view.
        """
        self.search_box.clear()  # Clear text
        self.populate_orders()  # Reload all orders
