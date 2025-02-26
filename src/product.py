
class Product:
    def __init__(self, product_id=None, name="", supplier_id="", unit="", price=0.0, quantity=0):
        if price < 0:
            raise ValueError("Price cannot be negative.")
        if quantity < 0:
            raise ValueError("Quantity cannot be negative.")
        
        self.product_id = product_id
        self.name = name
        self.supplier_id = supplier_id
        self.unit = unit
        self.price = price
        self.quantity = quantity

    def __str__(self):
        return f"Product ID: {self.product_id}, Name: {self.name}, Supplier ID: {self.supplier_id}, Unit: {self.unit}, Price: {self.price}, Quantity: {self.quantity}"

    def update_quantity(self, amount):
        self.quantity += amount

    def to_dict(self):
        return {
            'product_id': self.product_id,
            'name': self.name,
            'supplier_id': self.supplier_id,
            'unit': self.unit,
            'price': self.price,
            'quantity': self.quantity
        }