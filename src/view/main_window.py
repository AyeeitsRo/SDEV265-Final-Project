from PyQt6.QtWidgets import (
    QMainWindow, QVBoxLayout, QWidget, QLabel, QFrame,
    QHBoxLayout, QApplication, QScrollArea
)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt

from sidebar import *
from model.order import OrderManager


class MainWindow(QMainWindow):
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
        self.setWindowTitle("Inventory System")  # Sets title of window
        self.resize(1700, 1000)  # Sets window size
        
        self.order_manager = OrderManager()  # Order manager to access orders
        self.order_manager.seed_orders()

        # Obtains screen geometry
        screen = QApplication.primaryScreen()
        screen_geometry = screen.availableGeometry()
        # Calculates position to center the window
        x = (screen_geometry.width() - self.width()) // 2
        y = (screen_geometry.height() - self.height()) // 2
        # Sets the geometry of the window
        self.setGeometry(x, y, self.width(), self.height())
        
        # Set background color
        self.setStyleSheet('background-color: #FAF9F6;')  # Off White Color
        
        # Main Layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QHBoxLayout()
        main_widget.setLayout(main_layout)
        
        # Sidebar (navigation bar) 
        window_names = ['Home', 'Order Material', 'Inventory', 'Outgoing Work Orders', ]
        sidebar_frame = QFrame()  # Create a QFrame to wrap the Sidebar
        sidebar_frame.setFixedWidth(200)  # Match width with Sidebar

        # Create layout for the frame and add Sidebar to it
        frame_layout = QVBoxLayout()
        frame_layout.setContentsMargins(0, 0, 0, 0)
        frame_layout.setSpacing(0)

        sidebar = Sidebar(window_names, self.controller)
        frame_layout.addWidget(sidebar)
        sidebar_frame.setLayout(frame_layout)

        # Add the frame to the main layout
        main_layout.addWidget(sidebar_frame)
        
        # Main content layout (label)
        content_layout = QVBoxLayout()  # Create a vertical layout for the content
        main_layout.addLayout(content_layout)  # Add the content layout to the main layout
        
        # Add main label overhead
        self.label = QLabel("📦 Inventory System Dashboard")  # Title for the page
        self.label.setFont(QFont("Roboto", 32))
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setStyleSheet('color: #228B22;')
        content_layout.addWidget(self.label)

        # --- DASHBOARD CARDS ---
        dashboard_layout = QVBoxLayout()
        dashboard_layout.addStretch()
        content_layout.addLayout(dashboard_layout)
        
        # Orders to Be Verified
        orders_box = self.create_info_box(
            title = "✅ Orders to Be Verified",
            color = "#228B22",
            background = "#E6F4EA"
        )
        dashboard_layout.addWidget(orders_box)

        self.pending_orders_layout = QVBoxLayout()  # Layout to show pending orders
        self.pending_orders_layout = orders_box.layout()

        # Populate Pending Orders (after loading order data)
        self.populate_pending_orders()

        # Inventory Arriving Soon
        arriving_box = self.create_info_box(
            title = "🚚 Inventory Arriving Soon",
            color = "#FF8F00",
            background = "#FFF8E1"
        )
        dashboard_layout.addWidget(arriving_box)

        # Low Inventory Alerts
        alerts_box = self.create_info_box(
            title = "⚠️ Low Inventory Alerts",
            color = "#D32F2F",
            background = "#FDECEA"
        )
        dashboard_layout.addWidget(alerts_box)

    def populate_pending_orders(self):
        """
        Populates the 'Orders to be Verified' section with orders awaiting approval.
        """
        # Create a QWidget to hold the order widgets
        orders_container = QWidget()
        orders_layout = QVBoxLayout(orders_container)  # Use a new layout for the container
        
        orders = self.order_manager.get_orders()

        # Filter orders that are Pending
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
            order_label.setStyleSheet("""
                                    font-size: 18px; 
                                    color: #000000;
                                    border: none;
                                    """)
            
            order_layout.addWidget(order_label)
            order_layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
            order_widget.setLayout(order_layout)
            orders_layout.addWidget(order_widget)

        # Now create a QScrollArea and set it as the scrollable widget
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)  # Ensure the widget inside scroll area is resizable
        scroll_area.setWidget(orders_container)  # Set the orders container widget as the scrollable widget
        
        # Add the scroll area to the main content layout
        self.pending_orders_layout.addWidget(scroll_area)




    def create_info_box(self, title, color, background):
        box = QFrame()
        box.setStyleSheet(f"""
            QFrame {{
                background-color: {background};
                border: none;
            }}
        """)
        box.setFixedSize(1000, 250)  # Wider and taller box

        layout = QVBoxLayout()
        label = QLabel(title)
        label.setFont(QFont("Roboto", 16, QFont.Weight.Bold))
        label.setStyleSheet(f"color: {color};")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(label)
        box.setLayout(layout)

        return box
