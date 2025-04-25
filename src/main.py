import sys
from PyQt6.QtWidgets import QApplication
import view.login_window as login

"""
**main.py - Program execution file**

**Purpose**
- 
"""
if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    window = login.LoginWindow() # Creates the login window
    window.show() # Displays the main window
    
    sys.exit(app.exec()) # Starts the event loop
    
