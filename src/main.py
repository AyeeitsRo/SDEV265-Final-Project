import sys
from PyQt6.QtWidgets import QApplication
import view.main_window as mw
import controller.controller as ctr

"""
**main.py - Program execution file**

**Purpose**
- 
"""
if __name__ == "__main__":
    app = QApplication(sys.argv) # Initializes QApplication
    
    controller = ctr.Controller() # Initializes the controller
    window = mw.MainWindow(controller) # Creates the main window
    window.show() # Displays the main window
    
    sys.exit(app.exec()) # Starts the event loop