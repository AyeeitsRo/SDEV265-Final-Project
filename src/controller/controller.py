from PyQt6.QtWidgets import QApplication

from sidebar import *
from view.inventory_window import *
from view.main_window import *
from view.order_window import *
from view.inventory_order_window import *
from model.sku_order import handle_order_submission


class Controller:
    """
    **Controller Class**
    
    **Purpose**
    - Manages interactions between the different views and user events in the GUI.
    - The 'Communicator' between the **model** and **view** which are the logic and GUI Displays seperated.
    
    
    """
    def __init__(self):
        """Initalize the controller """ 
    
    def open_home(self):
        """Open home window"""
        self.home_view = MainWindow(self)
        self.home_view.show()
        
            
    def open_order(self):
        """Open order window"""
        self.order_view = OrderWindow(self)
        self.order_view.show()
    
    def open_search(self):
        """Open search window"""
        self.search_view = InventoryOrderWindow(self)
        self.search_view.show()
    
    def open_inventory(self):
        """Open inventory window"""
        self.inventory_view = InventoryWindow(self)
        self.inventory_view.show()
    
    def exit_app(self):
        """Stops application from running"""
        QApplication.quit()
        
    def clear_search(self):
        """Clear the search box and reset the table data in the inventory view."""
        if self.inventory_view:
            self.inventory_view.clear_search()
            
    def handle_submit(self, view):
        """Handle the submit button click from InventoryOrderWindow."""
        handle_order_submission(view)
        