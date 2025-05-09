# Contractor Plus – Inventory Management System

A desktop application built with **Python** and **PyQt6** for managing inventory, tracking orders, and monitoring stock levels for a small construction retail business.

## 🔧 Features

- **Inventory Management**  
  Track tools and construction items with fields like name, description, SKU, price, and quantity.

- **Order Management**  
  View and manage orders with details such as order ID, arrival date, status, and number of items.

- **Low Inventory Alerts**  
  Automatic detection and highlighting of items with zero or low quantity.

- **Dashboard Overview**  
  Displays pending orders, arriving inventory, and low-stock alerts in one unified main window.

- **MVC Architecture**  
  Logic, views, and controller code are cleanly separated for maintainability.

## 📁 Project Structure

SDEV265-FINAL-PROJECT/
├── resources/
│ ├── company-logo.png
│ └── home-banner.jpg
│
├── src/
│ ├── main.py
│ ├── sidebar.py
│ │
│ ├── controller/
│ │ └── controller.py
│ │
│ ├── model/
│ │ ├── incoming_orders.py
│ │ ├── inventory.py
│ │ ├── inventory_data.py
│ │ ├── order.py
│ │ └── sku_order.py
│ │
│ └── view/
│ ├── inventory_order_window.py
│ ├── inventory_window.py
│ ├── login_window.py
│ ├── main_window.py
│ └── order_window.py


## 🖥️ Installation

### Prerequisites

- Python 3.10 or newer recommended  
- pip package manager

### Step-by-Step

```bash
# 1. Clone the repository
git clone https://github.com/AyeeitsRo/SDEV265-Final-Project
cd SDEV265-Final-Project

# 2. Create a virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate    # On Windows use: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the application
python main.py
