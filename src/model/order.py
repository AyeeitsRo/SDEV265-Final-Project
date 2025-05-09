class Order:
    def __init__(self, order_id, date, shipping_type, price, status="Pending"):
        """
        Initializes an order with ID, date, shipping type, price, and status.
        Default status is 'Pending' if not provided.
        """
        self.order_id = order_id  # Store the order's unique ID
        self.date = date  # Store the order's date as a string
        self.shipping_type = shipping_type  # Store the shipping type (Standard, Express, etc.)
        self.price = price  # Store the price of the order
        self.status = status  # Store the order's status (default to 'Pending')

    def change_status(self, new_status):
        """
        Changes the status of the order.
        """
        self.status = new_status  # Update the order's status to the new value

    def __str__(self):
        """
        String representation of the order for easy printing.
        """
        return f"ID: {self.order_id} | Date: {self.date} | Shipping: {self.shipping_type} | Price: ${self.price:.2f} | Status: {self.status}"

class OrderManager:
    def __init__(self):
        """
        Initializes an OrderManager instance with an empty list of orders.
        """
        self.orders = []  # List to hold all the orders managed by this instance

    def add_order(self, order: Order):
        """
        Adds a new order to the orders list.
        """
        self.orders.append(order)  # Add the provided order to the list of orders

    def get_orders(self):
        """
        Returns the orders sorted by date (newest first).
        """
        return sorted(self.orders, key=lambda x: x.date, reverse=True)  # Sort orders by date in descending order

    def get_order_by_id(self, order_id):
        """
        Returns the order that matches the provided order ID.
        If no order is found, returns None.
        """
        for order in self.orders:
            if order.order_id == order_id:
                return order  # Return the matching order
        return None  # Return None if no matching order is found
    
    def seed_orders(self):
        """
        Seeds the orders list with hardcoded order data for testing or initial setup.
        """
        # Sample order data as tuples (order_id, date, shipping_type, price, status)
        orders_data = [
            ("ORD123", "2025-04-10", "Standard", 45.99, "Delivered"),
            ("ORD124", "2025-04-11", "Express", 99.49, "Delivered"),
            ("ORD125", "2025-04-12", "Standard", 34.76, "Delivered"),
            ("ORD126", "2025-04-15", "Air", 89.65, "Delivered"),
            ("ORD127", "2025-04-17", "Overnight", 156.23, "Delivered"),
            ("ORD128", "2025-04-18", "Standard", 1564.56, "Delivered"),
            ("ORD129", "2025-04-19", "Express", 274.89, "Delivered"),
            ("ORD130", "2025-04-20", "Standard", 67.45, "Delivered"),
            ("ORD131", "2025-04-21", "Air", 512.30, "Delivered"),
            ("ORD132", "2025-04-22", "Overnight", 321.99, "Delivered"),
            ("ORD133", "2025-04-23", "Standard", 278.00, "Delivered"),
            ("ORD134", "2025-04-24", "Express", 899.99, "Delivered"),
            ("ORD135", "2025-04-25", "Air", 1034.56, "Delivered"),
            ("ORD136", "2025-04-26", "Overnight", 425.65, "Delivered"),
            ("ORD137", "2025-04-27", "Standard", 121.70, "Delivered"),
            ("ORD138", "2025-04-28", "Express", 1350.45, "Delivered"),
            ("ORD139", "2025-04-29", "Air", 199.89, "Pending"),
            ("ORD140", "2025-04-30", "Overnight", 465.30, "Delivered"),
            ("ORD141", "2025-05-01", "Standard", 76.22, "Pending"),
            ("ORD142", "2025-05-02", "Express", 154.50, "Shipped"),
            ("ORD143", "2025-05-03", "Air", 875.80, "Processing"),
            ("ORD144", "2025-05-04", "Overnight", 654.35, "Delivered"),
            ("ORD145", "2025-05-05", "Standard", 48.99, "Shipped"),
            ("ORD146", "2025-05-06", "Express", 264.55, "Delivered"),
            ("ORD147", "2025-05-07", "Air", 340.80, "Shipped"),
            ("ORD148", "2025-05-08", "Overnight", 199.95, "Delivered"),
            ("ORD149", "2025-05-09", "Standard", 550.33, "Shipped"),
            ("ORD150", "2025-05-10", "Express", 1234.80, "Pending"),
            ("ORD151", "2025-05-11", "Air", 657.20, "Delivered"),
            ("ORD152", "2025-05-12", "Overnight", 782.11, "Delivered"),
            ("ORD153", "2025-05-13", "Standard", 899.95, "Pending"),
            ("ORD154", "2025-05-14", "Express", 389.60, "Pending"),
            ("ORD155", "2025-05-15", "Overnight", 512.75, "Pending"),
        ]

        # Add each seed order to the orders list
        for order_data in orders_data:
            # Each order_data is a tuple with order_id, date, shipping_type, price, and status
            self.add_order(Order(order_data[0], order_data[1], order_data[2], order_data[3], order_data[4]))
