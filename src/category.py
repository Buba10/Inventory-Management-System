class Category:
    def __init__(self, category_id, name):
        self.category_id = category_id
        self.name = name
        self.products = []

    def add_product(self, product):
        """Add a product to this category."""
        self.products.append(product)
        print(f"Product '{product.name}' added to category '{self.name}'.")

    def remove_product(self, product_id):

        """Remove a product from this category based on its ID."""

        for product in self.products:
            if product.product_id == product_id:
                self.products.remove(product)
                print(f"Product ID {product_id} removed from category '{self.name}'.")
                return
        print(f"Product ID {product_id} not found in category '{self.name}'.")

    def view_products(self):

        """View all products in this category."""

        if not self.products:
            print(f"No products found in category '{self.name}'.")
            return
        print(f"Products in category '{self.name}':")
        for product in self.products:
            print(f"ID: {product.product_id}, Name: {product.name}, Quantity: {product.quantity}, Price: ${product.price:.2f}")

    def update_product(self, product_id, quantity=None, price=None):

        """Update product details in this category based on its ID."""

        for product in self.products:
            if product.product_id == product_id:
                if quantity is not None:
                    product.quantity = quantity
                if price is not None:
                    product.price = price
                print(f"Product ID {product_id} updated successfully in category '{self.name}'.")
                return
        print(f"Product ID {product_id} not found in category '{self.name}'.")

    def __str__(self):

        """String representation of the category."""

        return f"Category ID: {self.category_id}, Name: {self.name}"