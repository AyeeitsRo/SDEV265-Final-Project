from PyQt6.QtWidgets import QApplication

from sidebar import *


class Controller:
    """
    **Controller Class**
    
    **Purpose**
    - Manages interactions between the different views and user events in the GUI.
    - The 'Communicator' between the **model** and **view** which are the logic and GUI Displays seperated.
    
    
    """
    def __init__(self):
        """Initalize the controller """ # SHOULD load whatever is on main window if anything
        pass
    
    def exit_app(self):
        print('Exiting System.')
        QApplication.quit()