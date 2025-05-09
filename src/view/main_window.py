
from PyQt6.QtWidgets import (
    QMainWindow, QVBoxLayout, QWidget, QLabel, QFrame,
    QHBoxLayout, QApplication, QScrollArea, QStackedLayout
)
from PyQt6.QtGui import QFont, QPixmap
from PyQt6.QtCore import Qt

from sidebar import Sidebar
from model.order import OrderManager
from model.inventory_data import inventory_data
from model.incoming_orders import orders


class MainWindow(QMainWindow):
    """
    Main dashboard window for the inventory system application.
    Displays:
    - A sidebar with navigation buttons.
    - Dashboard cards for pending orders, arriving inventory, and low stock alerts.
    """

    def __init__(self, controller: object) -> None:
        super().__init__()

        self.controller = controller  # Reference to the main controller for window navigation
        self.setWindowTitle("Inventory System")  # Set window title
        self.resize(1700, 1000)  # Default window size

        # === Initialize order data ===
        self.order_manager = OrderManager()
        self.order_manager.seed_orders()  # Populate with dummy orders

        # === Center the window on the screen ===
        screen = QApplication.primaryScreen()
        screen_geometry = screen.availableGeometry()
        x = (screen_geometry.width() - self.width()) // 2
        y = (screen_geometry.height() - self.height()) // 2
        self.setGeometry(x, y, self.width(), self.height())

        # === Set overall background color ===
        self.setStyleSheet('background-color: #FAF9F6;')

        # === Root widget and main horizontal layout ===
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QHBoxLayout()
        main_widget.setLayout(main_layout)

        # === Sidebar setup ===
        window_names = ['Home', 'Order Material', 'Inventory', 'Outgoing Work Orders']
        sidebar_frame = QFrame()
        sidebar_frame.setFixedWidth(200)  # Sidebar width

        frame_layout = QVBoxLayout()
        frame_layout.setContentsMargins(0, 0, 0, 0)
        frame_layout.setSpacing(0)
        sidebar = Sidebar(window_names, self.controller)
        frame_layout.addWidget(sidebar)
        sidebar_frame.setLayout(frame_layout)
        main_layout.addWidget(sidebar_frame)

        # === Content area (title + dashboard) ===
        content_layout = QVBoxLayout()
        main_layout.addLayout(content_layout)


        # === Banner frame with background image ===
        banner_frame = QFrame()
        banner_frame.setFixedHeight(180)

        # Background image label
        banner_image_label = QLabel()
        banner_image_label.setPixmap(
            QPixmap("resources/home-banner.jpg").scaledToHeight(
                390, Qt.TransformationMode.SmoothTransformation
            )
        )
        banner_image_label.setAlignment(Qt.AlignmentFlag.AlignLeft)

        banner_layout = QStackedLayout()
        banner_layout.addWidget(banner_image_label)
        banner_frame.setLayout(banner_layout)

        # Add to your existing layout
        content_layout.addWidget(banner_frame)

        # Layout for dashboard info cards
        dashboard_layout = QVBoxLayout()
        dashboard_layout.addStretch()  # Push cards to the top
        content_layout.addLayout(dashboard_layout)

        # === Dashboard Card: Pending Orders ===
        orders_box = self.create_info_box(
            title = "Orders to Be Verified",
            color = "#228B22",
            background = "#E6F4EA"
        )
        orders_box.setFixedWidth(1550)
        dashboard_layout.addWidget(orders_box)
        self.pending_orders_layout: QVBoxLayout = orders_box.layout()
        self.populate_pending_orders()  # Fill in pending orders

        # === Dashboard Card: Arriving Soon ===
        arriving_box = self.create_info_box(
            title = "Inventory Arriving Soon",
            color = "#FF8F00",
            background = "#FFF8E1"
        )
        arriving_box.setFixedWidth(1550)
        dashboard_layout.addWidget(arriving_box)
        self.arriving_orders_layout: QVBoxLayout = arriving_box.layout()
        self.populate_arriving_soon_orders()  # Fill in arriving inventory

        # === Dashboard Card: Low Inventory ===
        self.low_inventory_box: QFrame = self.create_info_box(
            title = "Low Inventory Alerts",
            color = "#D32F2F",
            background = "#FDECEA"
        )
        self.low_inventory_box.setFixedWidth(1550)
        dashboard_layout.addWidget(self.low_inventory_box)
        self.populate_low_inventory()  # Fill in low stock items

    def populate_pending_orders(self) -> None:
        """
        Populate the 'Pending Orders' card with order entries that need approval.
        """
        orders_container = QWidget()  # Container for the scroll area
        orders_layout = QVBoxLayout(orders_container)

        # Fetch all orders marked as 'Pending'
        orders = self.order_manager.get_orders()
        pending_orders = [order for order in orders if order.status == "Pending"]

        if not pending_orders:
            # Display message if no pending orders
            no_orders_label = QLabel("No orders awaiting approval.")
            no_orders_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            orders_layout.addWidget(no_orders_label)

        # Create a widget for each pending order
        for order in pending_orders:
            order_widget = QWidget()
            order_widget.setStyleSheet("background-color: #E6F4EA;")
            order_layout = QVBoxLayout()

            # Format: Order ID and its status
            order_label = QLabel(f"Order ID: {order.order_id} - Awaiting Approval")
            order_label.setStyleSheet("font-size: 18px; color: #000000;")
            order_layout.addWidget(order_label)

            order_widget.setLayout(order_layout)
            orders_layout.addWidget(order_widget)

        # Scroll area to contain the full list of orders
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(orders_container)
        self.pending_orders_layout.addWidget(scroll_area)

    def populate_arriving_soon_orders(self) -> None:
        """
        Populate the 'Inventory Arriving Soon' card with shipped orders.
        """
        arriving_soon_orders = [order for order in orders if order["status"] == "Shipped"]

        container = QWidget()  # Scrollable container widget
        layout = QVBoxLayout(container)

        if not arriving_soon_orders:
            # Display message if nothing is arriving soon
            no_orders_label = QLabel("No arriving orders found.")
            no_orders_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(no_orders_label)

        # For each arriving order, show a label with order ID and arrival date
        for order in arriving_soon_orders:
            label = QLabel(f"Order Number: {order['id']} — Arriving on {order['arrival']}")
            label.setStyleSheet("font-size: 18px; color: black;")
            layout.addWidget(label)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(container)
        self.arriving_orders_layout.addWidget(scroll_area)

    def populate_low_inventory(self) -> None:
        """
        Populate the 'Low Inventory Alerts' card with SKUs that have zero quantity.
        """
        low_inventory_items = [item for item in inventory_data if item[4] == 0]

        container = QWidget()
        container_layout = QVBoxLayout(container)

        if not low_inventory_items:
            # If no items are low, show a positive message
            no_label = QLabel("No items need to be reordered.")
            no_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            no_label.setStyleSheet("color: black; font-size: 16px;")
            container_layout.addWidget(no_label)

        # For each item with 0 quantity, display a warning
        for item in low_inventory_items:
            sku_label = QLabel(f"SKU: {item[2]} needs to be reordered!")
            sku_label.setStyleSheet("font-size: 18px; color: black;")
            sku_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
            container_layout.addWidget(sku_label)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(container)

        layout = self.low_inventory_box.layout()
        if layout:
            # Clear previous widgets in the layout before updating
            while layout.count():
                item = layout.takeAt(0)
                if item.widget():
                    item.widget().deleteLater()

            # Re-add section title and new scroll content
            title_label = QLabel("⚠️ Low Inventory Alerts")
            title_label.setFont(QFont("Roboto", 16, QFont.Weight.Bold))
            title_label.setStyleSheet("color: #D32F2F;")
            title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(title_label)
            layout.addWidget(scroll_area)

    def create_info_box(self, title: str, color: str, background: str) -> QFrame:
        """
        Creates a styled information box with a colored background and title.

        Args:
            title (str): The title text displayed at the top of the box.
            color (str): The text color used for the title.
            background (str): The background color of the card.

        Returns:
            QFrame: The completed styled box with a vertical layout.
        """
        box = QFrame()  # Main container frame
        box.setStyleSheet(f"""
            QFrame {{
                background-color: {background};
                border: none;
            }}
        """)
        box.setFixedSize(1000, 250)  # Card size

        layout = QVBoxLayout()  # Layout for contents
        label = QLabel(title)  # Title label
        label.setFont(QFont("Roboto", 16, QFont.Weight.Bold))
        label.setStyleSheet(f"color: {color};")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(label)
        box.setLayout(layout)

        return box
