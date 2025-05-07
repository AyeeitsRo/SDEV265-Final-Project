from PyQt6.QtWidgets import QApplication

from view.inventory_window import InventoryWindow
from view.main_window import MainWindow
from view.order_window import OrderWindow
from view.inventory_order_window import InventoryOrderWindow
from model.sku_order import handle_order_submission


class Controller:
    """
    Controller Class

    Purpose:
    Acts as the central hub for GUI navigation and user interaction in the application.
    
    Responsibilities:
    - Routes user actions (like button clicks) to the appropriate view logic.
    - Instantiates and displays different views: MainWindow, OrderWindow, InventoryWindow, and InventoryOrderWindow.
    - Handles coordination between the views and the backend logic (model layer).
    
    """
    def __init__(self) -> None:
        """Initialize the Controller."""
        self.home_view: MainWindow
        self.order_view: OrderWindow
        self.search_view: InventoryOrderWindow
        self.inventory_view: InventoryWindow 

    def open_home(self) -> None:
        """Open the main/home window."""
        self.home_view = MainWindow(self)
        self.home_view.show()

    def open_order(self) -> None:
        """Open the outgoing orders window."""
        self.order_view = OrderWindow(self)
        self.order_view.show()

    def open_search(self) -> None:
        """Open the inventory ordering/search window."""
        self.search_view = InventoryOrderWindow(self)
        self.search_view.show()

    def open_inventory(self) -> None:
        """Open the inventory view window."""
        self.inventory_view = InventoryWindow(self)
        self.inventory_view.show()

    def exit_app(self) -> None:
        """Quit the application."""
        QApplication.quit()

    def clear_search(self) -> None:
        """Clear the search input and reset inventory table data."""
        if self.inventory_view:
            self.inventory_view.clear_search()

    def handle_submit(self, view: InventoryOrderWindow) -> None:
        """
        Handle the submission of an order.

        Args:
            view (InventoryOrderWindow): The view containing the submit button and order form.
        """
        handle_order_submission(view)