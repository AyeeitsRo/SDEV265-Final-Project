from datetime import datetime

class Order:
    def __init__(self, order_id, date, shipping_type, price, status="Pending"):
        self.order_id = order_id
        self.date = date
        self.shipping_type = shipping_type
        self.price = price
        self.status = status

    def change_status(self, new_status):
        self.status = new_status

    def __str__(self):
        return f"ID: {self.order_id} | Date: {self.date} | Shipping: {self.shipping_type} | Price: ${self.price:.2f} | Status: {self.status}"


class OrderManager:
    def __init__(self):
        self.orders = []

    def add_order(self, order: Order):
        self.orders.append(order)

    def get_orders(self):
        return self.orders

    def get_order_by_id(self, order_id):
        for order in self.orders:
            if order.order_id == order_id:
                return order
        return None
