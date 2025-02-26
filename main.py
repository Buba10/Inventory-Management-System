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

        # Insert the new product into the database
        with self.connection.cursor() as cursor:
            try:
                cursor.execute(
                    "INSERT INTO products (ProductName, SupplierID, Unit, Price, Quantity) VALUES (%s, %s, %s, %s, %s)",
                    (new_product.name, new_product.supplier_id, new_product.unit, new_product.price, new_product.quantity)
                )
                self.connection.commit()
                print("Product added successfully!")
            except mysql.connector.Error as err:
                print(f"Error: {err}")

    def view_inventory(self):
        """Fetch and display all products from the database."""
        cursor = self.connection.cursor(dictionary=True)
        try:
            cursor.execute("SELECT ProductID, ProductName, SupplierID, Unit, Price, Quantity FROM products")
            products = cursor.fetchall()
            if products:
                for product in products:
                    print(f"ID: {product['ProductID']}, Name: {product['ProductName']}, "
                          f"Supplier ID: {product['SupplierID']}, Unit: {product['Unit']}, "
                          f"Price: ${product['Price']:.2f}, Quantity: {product['Quantity']}")
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

def main():
    inventory_management = InventoryManagement()

    while True:
        print("\nInventory Management System")
        print("1. Add Product")
        print("2. View Products")
        print("3. Update Product")
        print("4. Delete Product")
        print("5. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            inventory_management.add_product()

        elif choice == '2':
            inventory_management.view_inventory()

        elif choice == '3':
            product_id = int(input("Enter Product ID to update: "))
            quantity_input = input("Enter new quantity (or leave blank to skip): ")
            quantity = int(quantity_input) if quantity_input else None
            price_input = input("Enter new price (or leave blank to skip): ")
            price = float(price_input) if price_input else None
            inventory_management.update_product(product_id, quantity, price)

        elif choice == '4':
            product_id = int(input("Enter Product ID to delete: "))
            inventory_management.delete_product(product_id)

        elif choice == '5':
            inventory_management.close_connection()
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()