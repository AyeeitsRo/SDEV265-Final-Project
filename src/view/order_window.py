
from PyQt6.QtWidgets import (
    QPushButton, QVBoxLayout, QWidget, QLabel, QHeaderView,
    QHBoxLayout, QApplication, QTableWidget, QTableWidgetItem,
    QComboBox, 
)
from PyQt6.QtGui import QFont, QPixmap
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor

from sidebar import *
from model.order import Order, OrderManager


class OrderWindow(QWidget):
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
        
        self.order_manager = OrderManager() 
        
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
        window_names = ['Home', 'Search Products', 'Inventory', 'Orders',]
        sidebar = Sidebar(window_names, self.controller)
        main_layout.addWidget(sidebar)
        
        # Main content layout (label)
        content_layout = QVBoxLayout()  # Create a vertical layout for the content
        main_layout.addLayout(content_layout)  # Add the content layout to the main layout
        
        # Add main label overhead
        self.label = QLabel("Orders") # Sets the text inside the label
        self.label.setFont(QFont("Roboto", 32)) # Sets label in "roboto" style with a 32 point font
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter) # Centers the label
        self.label.setStyleSheet('color: #228B22;') # Sets label text color to dark green
        content_layout.addWidget(self.label)
        
        
        # Create table to hold order data
        self.order_table = QTableWidget() # Create table
        self.order_table.setColumnCount(5) # Set amount of columns
        self.order_table.setHorizontalHeaderLabels(["Order ID", "Date", "Shipping", "Price", "Status"]) # Set header names
        # Style table header
        self.order_table.setStyleSheet("""
            QHeaderView::section {
                background-color: #228B22;
                color: black;
                font-weight: italic;
                font-size: 11pt;
                font-family: Roboto;
                padding: 4px;
            }
        """)
        self.order_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)  # Make cells read-only
        self.order_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.order_table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.order_table.horizontalHeader().setStretchLastSection(True)
        self.order_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        
        self.order_table.horizontalHeader().setStyleSheet("background-color: #228B22; color: #228B22;")
        self.order_table.horizontalHeader().setVisible(True)

        content_layout.addWidget(self.order_table)        
           
        self.populate_orders()
        self.seed_orders()


        
        
    def seed_orders(self):
        self.order_manager.add_order(Order("ORD123", "2025-04-10", "Standard", 45.99))
        self.order_manager.add_order(Order("ORD124", "2025-04-11", "Express", 99.49))
        self.order_manager.add_order(Order("ORD125", "2025-04-12", "Standard", 34.76))
        self.populate_orders()



    def populate_orders(self):
        self.order_table.setRowCount(0)
        orders = self.order_manager.get_orders()
        self.order_table.setRowCount(len(orders))

        for row, order in enumerate(orders):
            data = [order.order_id, order.date, order.shipping_type, f"${order.price:.2f}"]

            for col, value in enumerate(data):
                item = QTableWidgetItem(str(value))
                item.setForeground(QColor("black"))
                font = item.font()
                font.setPointSize(10)

                if col == 4 and order.status == "Delivered":
                    item.setForeground(Qt.GlobalColor.darkGreen)
                    font.setBold(True)

                item.setFont(font)
                self.order_table.setItem(row, col, item)

            # Add dropdown (QComboBox) to last column
            combo = QComboBox()
            combo.addItems(["Pending", "Processing", "Shipped", "Delivered"])
            combo.setCurrentText(order.status)
            combo.setStyleSheet("background-color: white; color: black; font-size: 10pt;")

            # Connect status change event
            combo.currentTextChanged.connect(lambda new_status, row=row: self.change_order_status(row, new_status))
            self.order_table.setCellWidget(row, 4, combo)


    def change_order_status(self, row, new_status):
        order_id = self.order_table.item(row, 0).text()
        order = self.order_manager.get_order_by_id(order_id)
        if order and order.status != new_status:
            order.change_status(new_status)
            self.populate_orders()



        


