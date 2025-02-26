import sys
import os
import mysql.connector

# Set the path to the src directory
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src'))


from product import Product
from category import Category

# Database configuration
db_config = {
    'host': 'localhost',
    'user': 'Buba',
    'password': 'Xcellerate-1',
    'database': 'db_InventoryManagement',
}


class InventoryManagement:
    def __init__(self):
        self.connection = self.connect_to_database()
        self.products = {}

    def connect_to_database(self):
        """Establish a connection to the database."""
        try:
            connection = mysql.connector.connect(**db_config)
            if connection.is_connected():
                print("Database connection successful!")
                return connection
        except mysql.connector.Error as err:
            print(f"Error: {err}")
        return None

    def add_product(self):
        """Add a new product to the inventory."""
        product_name = input("Enter product name: ")
        supplier_id = input("Enter Supplier ID: ")
        unit = input("Enter unit: ")
        price = float(input("Enter price: "))  # Convert to float for price
        quantity = int(input("Enter quantity: "))  # Convert to int for quantity

        # Create a new Product instance
        new_product = Product(None, product_name, supplier_id, unit, price, quantity)

        # Assuming you have a method to add the product to your inventory list
        self.products.append(new_product)  # Add the new product to the products list
        print("Product added successfully!")
    
    
    def view_inventory(self):
        """Fetch and display all products from the database."""
        cursor = self.connection.cursor(dictionary=True)
        try:
            cursor.execute("SELECT ProductID, ProductName, SupplierID, Unit, Price FROM products")
            products = cursor.fetchall()
            if products:
                for product in products:
                    print(f"ID: {product['ProductID']}, Name: {product['ProductName']}, "
                      f"Supplier ID: {product['SupplierID']}, Unit: {product['Unit']}, "
                      f"Price: ${product['Price']:.2f}")
            else:
                print("No products found in the inventory.")
        except mysql.connector.Error as err:
            print(f"Error: {err}")
        finally:
            cursor.close()
    def update_product(self, product_id, quantity=None, price=None):
        """Update a product's details."""
        with self.connection.cursor() as cursor:
            try:
                update_fields = []
                params = []

                if quantity is not None:
                    update_fields.append("Quantity = %s")
                    params.append(quantity)
                if price is not None:
                    update_fields.append("Price = %s")
                    params.append(price)

                params.append(product_id)  # Add product_id to the parameters

                if update_fields:
                    cursor.execute(
                        f"UPDATE products SET {', '.join(update_fields)} WHERE ProductID = %s",
                        tuple(params)
                    )
                    self.connection.commit()
                    print(f"Product ID {product_id} updated successfully.")
                else:
                    print("No updates provided.")
            except mysql.connector.Error as err:
                print(f"Error: {err}")

    def delete_product(self, product_id):
        """Delete a product from the inventory."""
        with self.connection.cursor() as cursor:
            try:
                cursor.execute("DELETE FROM products WHERE ProductID = %s", (product_id,))
                self.connection.commit()
                print(f"Product ID {product_id} deleted successfully.")
            except mysql.connector.Error as err:
                print(f"Error: {err}")

    def close_connection(self):
        """Close the database connection."""
        if self.connection.is_connected():
            self.connection.close()
            print("Database connection closed.")