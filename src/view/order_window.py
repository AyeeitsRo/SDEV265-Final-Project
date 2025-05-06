from PyQt6.QtWidgets import (
    QFrame, QVBoxLayout, QWidget, QLabel, QHeaderView,
    QHBoxLayout, QApplication, QTableWidget, QTableWidgetItem,
    QComboBox, QLineEdit, QPushButton
)
from PyQt6.QtGui import QFont, QPixmap
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor

from sidebar import *
from model.order import OrderManager


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
        self.order_manager.seed_orders() 
        
        # Obtains screen geometry
        screen = QApplication.primaryScreen()
        screen_geometry = screen.availableGeometry()
        x = (screen_geometry.width() - self.width()) // 2
        y = (screen_geometry.height() - self.height()) // 2
        self.setGeometry(x, y, self.width(), self.height())
        
        # Set background color
        self.setStyleSheet('background-color: #FAF9F6;')  # Off White Color
        
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
        main_layout.addWidget(sidebar_frame)
        
        # Main content layout
        content_layout = QVBoxLayout()
        main_layout.addLayout(content_layout)
        
        # Title Label
        self.label = QLabel("Work Orders")
        self.label.setFont(QFont("Roboto", 32))
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setStyleSheet('color: #228B22;')
        content_layout.addWidget(self.label)

        # --- Search Bar ---
        self.search_layout = QHBoxLayout()

        self.search_box = QLineEdit(self)
        self.search_box.setPlaceholderText("Search work orders...")
        self.search_box.setFixedWidth(400)
        self.search_box.setStyleSheet("""
            border: 2px solid #228B22;
            border-radius: 4px;
            padding: 5px;
            color: black;
        """)
        self.search_box.textChanged.connect(self.on_search)

        self.clear_button = QPushButton("Clear Search", self)
        self.clear_button.setFixedWidth(125)
        self.clear_button.setStyleSheet("""
            background-color: #228B22;
            color: white;
            border-radius: 4px;
            padding: 5px;
        """)
        self.clear_button.clicked.connect(self.clear_search)

        self.search_layout.addWidget(self.search_box)
        self.search_layout.addWidget(self.clear_button)
        self.search_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)

        content_layout.addLayout(self.search_layout)

        # --- Order Table ---
        self.order_table = QTableWidget()
        self.order_table.setColumnCount(5)
        self.order_table.setHorizontalHeaderLabels(["Order ID", "Date", "Shipping", "Price", "Status"])
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
        self.order_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.order_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.order_table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.order_table.verticalHeader().setVisible(False)
        self.order_table.horizontalHeader().setStretchLastSection(True)
        self.order_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        content_layout.addWidget(self.order_table)

        self.populate_orders()


    def populate_orders(self):
        self.populate_filtered_orders(self.order_manager.get_orders())


    def populate_filtered_orders(self, orders):
        self.order_table.setRowCount(0)
        self.order_table.setRowCount(len(orders))

        for row, order in enumerate(orders):
            data = [order.order_id, order.date, order.shipping_type, f"${order.price:.2f}"]

            for col, value in enumerate(data):
                item = QTableWidgetItem(str(value))
                item.setForeground(Qt.GlobalColor.darkGreen)
                font = item.font()
                font.setPointSize(10)
                font.setBold(True)
                item.setFont(font)
                self.order_table.setItem(row, col, item)
            
            combo = QComboBox()
            combo.addItems(["Pending", "Processing", "Shipped", "Delivered"])
            combo.setCurrentText(order.status)
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
            combo.currentTextChanged.connect(lambda new_status, row=row: self.change_order_status(row, new_status))
            self.order_table.setCellWidget(row, 4, combo)


    def change_order_status(self, row, new_status):
        order_id = self.order_table.item(row, 0).text()
        order = self.order_manager.get_order_by_id(order_id)
        if order and order.status != new_status:
            order.change_status(new_status)
            self.populate_orders()


    def on_search(self):
        query = self.search_box.text().lower()
        filtered_orders = []

        for order in self.order_manager.get_orders():
            row_data = [
                str(order.order_id),
                str(order.date),
                str(order.shipping_type),
                f"${order.price:.2f}",
                str(order.status)
            ]
            if any(query in field.lower() for field in row_data):
                filtered_orders.append(order)

        self.populate_filtered_orders(filtered_orders)


    def clear_search(self):
        self.search_box.clear()
        self.populate_orders()
