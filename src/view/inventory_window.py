from PyQt6.QtWidgets import (
    QFrame, QVBoxLayout, QWidget, QLabel, QHeaderView,
    QHBoxLayout, QApplication, QTableWidget, QTableWidgetItem,
    QLineEdit, QPushButton
)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt

from sidebar import *
from model.inventory import *

class InventoryWindow(QWidget):
    '''
    Inventory (Search) Window using same layout as OrderWindow
    '''
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.setWindowTitle("Inventory System")
        self.resize(1700, 1000)

        # Center window
        screen = QApplication.primaryScreen()
        screen_geometry = screen.availableGeometry()
        x = (screen_geometry.width() - self.width()) // 2
        y = (screen_geometry.height() - self.height()) // 2
        self.setGeometry(x, y, self.width(), self.height())

        self.setStyleSheet('background-color: #FAF9F6;')

        # Layouts
        main_layout = QHBoxLayout()
        self.setLayout(main_layout)

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

        content_layout = QVBoxLayout()
        main_layout.addLayout(content_layout)

        # Header
        self.label = QLabel("Inventory")
        self.label.setFont(QFont("Roboto", 32))
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setStyleSheet('color: #228B22;')
        content_layout.addWidget(self.label)

        # Search Bar
        self.search_layout = QHBoxLayout()

        # Search box
        self.search_box = QLineEdit(self)
        self.search_box.setPlaceholderText("Search inventory...")
        self.search_box.setFixedWidth(400)  # Set width to 1/4 of the screen
        self.search_box.setStyleSheet("""
            border: 2px solid #228B22;
            border-radius: 4px;
            padding: 5px;
            color: black;
        """)
        self.search_box.textChanged.connect(self.on_search)

        # Search button
        self.clear_button = QPushButton("Clear Search", self)
        self.clear_button.setFixedWidth(125) 
        self.clear_button.clicked.connect(self.clear_search)
        self.clear_button.setStyleSheet("""
            background-color: #228B22;
            color: white;
            border-radius: 4px;
            padding: 5px;
        """)

        self.search_layout.addWidget(self.search_box)
        self.search_layout.addWidget(self.clear_button)

        # Adjust alignment
        self.search_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        content_layout.addLayout(self.search_layout)

        # Table
        self.inventory_table = QTableWidget()
        self.inventory_table.setColumnCount(6)
        self.inventory_table.setHorizontalHeaderLabels(["#", "Item Name", "Description", "SKU", "Price", "Quantity"])
        
        header = self.inventory_table.horizontalHeader()
        font = QFont("Roboto", 11)
        font.setItalic(True)
        font.setBold(False)
        header.setFont(font)

        self.inventory_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.inventory_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.inventory_table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.inventory_table.verticalHeader().setVisible(False)
        self.inventory_table.horizontalHeader().setStretchLastSection(True)
        self.inventory_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        self.inventory_table.setAlternatingRowColors(True)
        self.inventory_table.setStyleSheet("""
                                           
            QTableWidget {
                alternate-background-color: #f0f0f0;
                background-color: white;
            }
                                           
            QHeaderView::section {
                background-color: #228B22;
                color: black;
                font-weight: italic;
                font-size: 11pt;
                font-family: Roboto;
                padding: 4px;
            }
            """)

        content_layout.addWidget(self.inventory_table)

        self.populate_inventory()

    def populate_inventory(self):
        self.inventory_data = [
                    ["Hammer", "16oz claw hammer", "HAM-0001", 14.99, 25],
                    ["Hammer", "20oz framing hammer", "HAM-0002", 19.99, 0],
                    ["Hammer", "Sledgehammer 10lb", "HAM-0003", 32.50, 7],
                    ["Screwdriver", "Flathead 4-inch", "SDR-0004", 4.25, 50],
                    ["Screwdriver", "Phillips 3-inch", "SDR-0005", 4.50, 42],
                    ["Screwdriver", "Precision set (6pc)", "SDR-0006", 9.75, 12],
                    ["Drill", "Cordless 18V drill", "DRL-0007", 59.99, 15],
                    ["Drill", "Corded drill 500W", "DRL-0008", 39.99, 5],
                    ["Drill", "Drill bit set (20pc)", "DRL-0009", 14.95, 0],
                    ["Wrench", "Adjustable wrench 8-inch", "WRN-0010", 7.99, 34],
                    ["Wrench", "Socket set (24pc)", "WRN-0011", 27.50, 13],
                    ["Wrench", "Torque wrench", "WRN-0012", 45.00, 6],
                    ["Pliers", "Needle nose", "PLR-0013", 6.75, 17],
                    ["Pliers", "Slip joint", "PLR-0014", 6.95, 28],
                    ["Pliers", "Linesman", "PLR-0015", 8.25, 11],
                    ["Tape Measure", "25ft locking", "TPM-0016", 5.99, 100],
                    ["Tape Measure", "100ft open reel", "TPM-0017", 15.99, 7],
                    ["Level", "24-inch spirit level", "LVL-0018", 12.99, 10],
                    ["Level", "Laser level kit", "LVL-0019", 49.99, 3],
                    ["Utility Knife", "Retractable", "KNF-0020", 4.99, 60],
                    ["Utility Knife", "Folding pocket knife", "KNF-0021", 6.25, 0],
                    ["Saw", "Hand saw 15-inch", "SAW-0022", 9.99, 19],
                    ["Saw", "Hacksaw", "SAW-0023", 7.99, 23],
                    ["Saw", "Circular saw 7.25-inch", "SAW-0024", 89.99, 4],
                    ["Sander", "Orbital sander", "SND-0025", 39.99, 6],
                    ["Sander", "Belt sander", "SND-0026", 44.99, 2],
                    ["Clamp", "C-clamp 4-inch", "CLP-0027", 3.25, 30],
                    ["Clamp", "Bar clamp 12-inch", "CLP-0028", 7.50, 14],
                    ["Clamp", "Spring clamp", "CLP-0029", 1.75, 40],
                    ["Gloves", "Nitrile work gloves", "GLV-0030", 1.50, 200],
                    ["Gloves", "Leather palm gloves", "GLV-0031", 3.25, 120],
                    ["Gloves", "Cut-resistant gloves", "GLV-0032", 6.75, 0],
                    ["Goggles", "Safety goggles", "GOG-0033", 4.50, 36],
                    ["Goggles", "Anti-fog wraparound", "GOG-0034", 6.25, 28],
                    ["Helmet", "Hard hat - white", "HMT-0035", 11.95, 20],
                    ["Helmet", "Hard hat - yellow", "HMT-0036", 11.95, 15],
                    ["Mask", "Dust mask (box of 20)", "MSK-0037", 14.99, 18],
                    ["Mask", "Respirator w/ filters", "MSK-0038", 24.99, 4],
                    ["Toolbox", "Plastic toolbox 16-inch", "TLB-0039", 12.95, 16],
                    ["Toolbox", "Metal toolbox 20-inch", "TLB-0040", 28.99, 0],
                    ["Cord", "50ft extension cord", "CRD-0041", 19.99, 8],
                    ["Cord", "100ft extension cord", "CRD-0042", 34.50, 0],
                    ["Flashlight", "LED rechargeable", "FLS-0043", 16.95, 11],
                    ["Flashlight", "Mini pocket light", "FLS-0044", 6.50, 29],
                    ["Chisel", "Wood chisel set (4pc)", "CHS-0045", 15.25, 10],
                    ["Chisel", "Cold chisel 8-inch", "CHS-0046", 5.99, 13],
                    ["Brush", "Wire brush", "BRH-0047", 2.25, 33],
                    ["Brush", "Paint brush 2-inch", "BRH-0048", 1.99, 48],
                    ["Ladder", "6ft fiberglass ladder", "LDR-0049", 79.99, 5],
                    ["Ladder", "10ft aluminum ladder", "LDR-0050", 119.99, 2],
                    ["Wheelbarrow", "6 cu ft steel", "WBR-0051", 89.99, 4],
                    ["Concrete", "Quick-mix 80lb bag", "CNM-0052", 6.50, 92],
                    ["Nails", "3-inch framing nails (5lb)", "NAL-0053", 7.99, 35],
                    ["Screws", "1.25in wood screws (box)", "SCR-0054", 5.25, 60],
                    ["Bolts", "3/8\" hex bolts (box)", "BLT-0055", 8.95, 45],
                    ["Tarps", "10x12 waterproof tarp", "TRP-0056", 9.99, 9],
                    ["Paint", "Interior flat white (gal)", "PNT-0057", 17.99, 26],
                    ["Paint", "Exterior weatherproof (gal)", "PNT-0058", 22.50, 14],
                    ["Paint Roller", "9-inch roller set", "PNR-0059", 7.95, 22],
                    ["Paint Tray", "Plastic tray", "PNY-0060", 2.75, 30],
                    ["Caulk", "Silicone white", "CLK-0061", 3.50, 80],
                    ["Caulk Gun", "Dripless", "CLG-0062", 6.99, 18],
                    ["Putty Knife", "Flexible 3-inch", "PTK-0063", 2.25, 27],
                    ["Measuring Wheel", "Distance measuring wheel", "MWL-0064", 49.99, 3],
                    ["Stud Finder", "Electronic stud finder", "STF-0065", 21.99, 6],
                    ["Work Light", "Tripod LED light", "WKL-0066", 34.99, 4],
                    ["Angle Grinder", "4.5\" angle grinder", "ANG-0067", 42.95, 8],
                    ["Circular Saw Blade", "7.25\" 24T", "BLD-0068", 9.25, 16],
                    ["PVC Pipe", "1\" x 10ft", "PVC-0069", 6.99, 42],
                    ["Copper Pipe", "3/4\" x 10ft", "CPR-0070", 22.00, 0],
                    ["Pipe Wrench", "14-inch", "PWR-0071", 18.50, 12],
                    ["Trowel", "Masonry trowel", "TRW-0072", 5.75, 20],
                    ["Shovel", "Round point", "SHV-0073", 14.99, 9],
                    ["Pickaxe", "36\" handle", "PCK-0074", 24.95, 3],
                    ["Rake", "24-tine leaf rake", "RAK-0075", 8.95, 10],
                    ["Wheel", "Replacement wheel 10\"", "WHL-0076", 11.50, 6],
                    ["Fuel Can", "5-gallon red", "FLC-0077", 17.99, 4],
                    ["Toolbelt", "Leather 11-pocket", "TLB-0078", 29.99, 15],
                    ["Hose", "Contractor garden hose 50ft", "HSE-0079", 21.95, 0],
                    ["Hose Nozzle", "Adjustable spray", "HSN-0080", 3.95, 24],
                    ["Tarp Clips", "Heavy duty clips (4)", "TPC-0081", 5.99, 13],
                    ["Ratcheting Straps", "2\" x 27ft (2 pack)", "RTS-0082", 18.50, 7],
                    ["Plastic Sheeting", "6 mil 10x25ft", "PLS-0083", 14.75, 5],
                    ["Bucket", "5-gallon heavy-duty", "BKT-0084", 3.50, 88],
                    ["Work Shirt", "Hi-vis long sleeve", "WKS-0085", 15.99, 20],
                    ["Ear Protection", "Over-ear muffs", "EPR-0086", 8.99, 17],
                    ["Knee Pads", "Foam padded", "KNP-0087", 9.50, 11],
                    ["Fence Post", "Steel 6ft", "FCP-0088", 7.25, 0],
                    ["Rebar", "1/2\" x 10ft", "RBR-0089", 6.50, 39],
                    ["Lumber", "2x4x8 SPF stud", "LMB-0090", 3.85, 94],
                    ["Drywall", "1/2\" x 4x8 sheet", "DRW-0091", 13.50, 40],
                    ["Insulation", "R-13 Kraft roll", "INS-0092", 34.99, 8],
                    ["Roofing Nails", "1.25in coil (7200ct)", "RFN-0093", 21.99, 26],
                    ["PVC Cement", "8oz blue", "PVC-0094", 4.99, 0],
                    ["Paint Masker", "Tape + film tool", "PMK-0095", 12.75, 10],
                    ["Wire Spool", "14/2 Romex 50ft", "WIR-0096", 36.50, 6],
                    ["Breaker", "15 amp single pole", "BRK-0097", 5.99, 17],
                    ["Outlet Box", "PVC 1-gang", "OTB-0098", 1.45, 60],
                    ["Switch", "Single pole toggle", "SWT-0099", 1.25, 80],
                    ["Light Bulb", "LED A19 60W equivalent", "LBL-0100", 1.99, 50],
                    ["Extension Ladder", "24ft aluminum", "LAD-0101", 179.00, 0],
                ]


        self.inventory_table.setRowCount(len(self.inventory_data))

        for row, item_data in enumerate(self.inventory_data):
            number_item = QTableWidgetItem(str(row + 1))
            number_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self._style_item(number_item)
            self.inventory_table.setItem(row, 0, number_item)

            for col, value in enumerate(item_data, start=1):
                item = QTableWidgetItem(str(value))
                self._style_item(item)
                self.inventory_table.setItem(row, col, item)


    def on_search(self):
        """Handles search action when the button is clicked."""
        query = self.search_box.text()  # Get the text from the search box
        filtered_data = search_inventory(query, self.inventory_data)  # Call the search function
        self.populate_filtered_inventory(filtered_data)

    def populate_filtered_inventory(self, filtered_data):
        """Populate the table with filtered data."""
        self.inventory_table.setRowCount(len(filtered_data))

        for row, item_data in enumerate(filtered_data):
            # Column 0: Row number
            number_item = QTableWidgetItem(str(row + 1))
            number_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self._style_item(number_item)
            self.inventory_table.setItem(row, 0, number_item)

            # Columns 1–5: Item Name, Description, SKU, Price, Quantity
            for col, value in enumerate(item_data, start=1):
                if col == 4:  # Price column (index 3 in data)
                    formatted_price = f"${value:.2f}"
                    item = QTableWidgetItem(formatted_price)
                else:
                    item = QTableWidgetItem(str(value))
                self._style_item(item)
                self.inventory_table.setItem(row, col, item)


    def _style_item(self, item):
        """Helper to apply consistent styling to table items"""
        item.setForeground(Qt.GlobalColor.darkGreen)
        font = item.font()
        font.setPointSize(10)
        font.setBold(True)
        item.setFont(font)
        
    def clear_search(self):
        """Clear the search box and reset the table data."""
        self.search_box.clear() 
        self.populate_inventory()  
