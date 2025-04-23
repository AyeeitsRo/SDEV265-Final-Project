from PyQt6.QtWidgets import QApplication

from sidebar import *
from view.inventory_window import *
from view.main_window import *
from view.order_window import *
from view.search_window import *


class Controller:
    """
    **Controller Class**
    
    **Purpose**
    - Manages interactions between the different views and user events in the GUI.
    - The 'Communicator' between the **model** and **view** which are the logic and GUI Displays seperated.
    
    
    """
    def __init__(self):
        """Initalize the controller """ 

        '''# Initialize views
        self.home_view = MainWindow(self)
        self.search_view = SearchWindow(self)
        self.order_view = OrderWindow(self)
        self.inventory_view = InventoryWindow(self)

        # Initialize stacked widget to hold views
        self.stacked_widget = QStackedWidget()
        self.stacked_widget.addWidget(self.home_view)
        self.stacked_widget.addWidget(self.order_view)
        self.stacked_widget.addWidget(self.search_view)
        self.stacked_widget.addWidget(self.inventory_view)

        # Set the stacked widget as the central widget
        if isinstance(self.home_view, QMainWindow):
            self.home_view.setCentralWidget(self.stacked_widget)'''
    
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
        self.search_view = SearchWindow(self)
        self.search_view.show()
    
    def open_inventory(self):
        """Open inventory window"""
        self.inventory_view = InventoryWindow(self)
        self.inventory_view.show()
    
    def exit_app(self):
        """Stops application from running"""
        print('Exiting System.')
        QApplication.quit()
        