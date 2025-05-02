from PyQt6.QtWidgets import (
    QMainWindow, QVBoxLayout, QWidget, QLabel, QFrame,
    QHBoxLayout, QApplication, QScrollArea
)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt

from sidebar import *

from model.order import OrderManager
from model.inventory_data import *
from model.incoming_orders import orders


class MainWindow(QMainWindow):
    '''
    The main window of the inventory system.
    '''
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.setWindowTitle("Inventory System")
        self.resize(1700, 1000)
        
        self.order_manager = OrderManager()
        self.order_manager.seed_orders()

        # Center window
        screen = QApplication.primaryScreen()
        screen_geometry = screen.availableGeometry()
        x = (screen_geometry.width() - self.width()) // 2
        y = (screen_geometry.height() - self.height()) // 2
        self.setGeometry(x, y, self.width(), self.height())

        self.setStyleSheet('background-color: #FAF9F6;')
        
        # Main Layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QHBoxLayout()
        main_widget.setLayout(main_layout)
        
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
        
        # Content Layout
        content_layout = QVBoxLayout()
        main_layout.addLayout(content_layout)

        # Title
        self.label = QLabel("📦 Inventory System Dashboard")
        self.label.setFont(QFont("Roboto", 32))
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setStyleSheet('color: #228B22;')
        content_layout.addWidget(self.label)

        # Dashboard Cards
        dashboard_layout = QVBoxLayout()
        dashboard_layout.addStretch()
        content_layout.addLayout(dashboard_layout)

        # Orders to Be Verified
        orders_box = self.create_info_box(
            title="✅ Orders to Be Verified",
            color="#228B22",
            background="#E6F4EA"
        )
        dashboard_layout.addWidget(orders_box)
        self.pending_orders_layout = orders_box.layout()
        self.populate_pending_orders()

        # Inventory Arriving Soon
        arriving_box = self.create_info_box(
            title="🚚 Inventory Arriving Soon",
            color="#FF8F00",
            background="#FFF8E1"
        )
        dashboard_layout.addWidget(arriving_box)
        self.arriving_orders_layout = arriving_box.layout()
        self.populate_arriving_soon_orders()

        # Low Inventory Alerts
        self.low_inventory_box = self.create_info_box(
            title="⚠️ Low Inventory Alerts",
            color="#D32F2F",
            background="#FDECEA"
        )
        dashboard_layout.addWidget(self.low_inventory_box)
        self.populate_low_inventory()

    def populate_pending_orders(self):
        orders_container = QWidget()
        orders_layout = QVBoxLayout(orders_container)
        orders = self.order_manager.get_orders()
        pending_orders = [order for order in orders if order.status == "Pending"]

        if not pending_orders:
            no_orders_label = QLabel("No orders awaiting approval.")
            no_orders_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            orders_layout.addWidget(no_orders_label)

        for order in pending_orders:
            order_widget = QWidget()
            order_widget.setStyleSheet("background-color: #E6F4EA;")
            order_layout = QVBoxLayout()
            order_label = QLabel(f"Order ID: {order.order_id} - Awaiting Approval")
            order_label.setStyleSheet("font-size: 18px; color: #000000;")
            order_layout.addWidget(order_label)
            order_widget.setLayout(order_layout)
            orders_layout.addWidget(order_widget)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(orders_container)
        self.pending_orders_layout.addWidget(scroll_area)

    def populate_arriving_soon_orders(self):
        # Filter orders that are 'Shipped'
        arriving_soon_orders = [order for order in orders if order["status"] == "Shipped"]

        container = QWidget()
        layout = QVBoxLayout(container)

        if not arriving_soon_orders:
            no_orders_label = QLabel("No arriving orders found.")
            no_orders_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(no_orders_label)

        for order in arriving_soon_orders:
            # Accessing the order details from the dictionary
            order_id = order["id"]
            arrival_date = order["arrival"]
            item_count = order["items"]

            # Creating the label to display Order ID and Arrival Date
            label = QLabel(f"Order Number: {order_id} — Arriving on {arrival_date}")
            label.setStyleSheet("font-size: 18px; color: black;")
            layout.addWidget(label)

        # Create a scroll area to allow the orders to be scrollable
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(container)

        # Now, add the scroll area to the arriving orders layout
        self.arriving_orders_layout.addWidget(scroll_area)

    def populate_low_inventory(self):
        low_inventory_items = [item for item in inventory_data if item[4] == 0]
        container = QWidget()
        container_layout = QVBoxLayout(container)

        if not low_inventory_items:
            no_low_inventory_label = QLabel("No items need to be reordered.")
            no_low_inventory_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            no_low_inventory_label.setStyleSheet("color: black; font-size: 16px;")
            container_layout.addWidget(no_low_inventory_label)

        for item in low_inventory_items:
            sku_label = QLabel(f"SKU: {item[2]} needs to be reordered!")
            sku_label.setStyleSheet("font-size: 18px; color: black;")
            sku_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
            container_layout.addWidget(sku_label)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(container)

        low_inventory_layout = self.low_inventory_box.layout()
        while low_inventory_layout.count():
            item = low_inventory_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        title_label = QLabel("⚠️ Low Inventory Alerts")
        title_label.setFont(QFont("Roboto", 16, QFont.Weight.Bold))
        title_label.setStyleSheet("color: #D32F2F;")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        low_inventory_layout.addWidget(title_label)
        low_inventory_layout.addWidget(scroll_area)

    def create_info_box(self, title, color, background):
        box = QFrame()
        box.setStyleSheet(f"""
            QFrame {{
                background-color: {background};
                border: none;
            }}
        """)
        box.setFixedSize(1000, 250)

        layout = QVBoxLayout()
        label = QLabel(title)
        label.setFont(QFont("Roboto", 16, QFont.Weight.Bold))
        label.setStyleSheet(f"color: {color};")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(label)
        box.setLayout(layout)

        return box
