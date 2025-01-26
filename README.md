# Warehouse Inventory System


## Flow charts:

``` mermaid
classDiagram
    class Product {
        + id : int
        + name : string
        + price : float
        + quantity : int
        + category : string
        + entry_date : date
        + exit_date : date
        +register_entry(self, quantity : int)
        +register_exit(self, quantity : int)
        +__str __(self)
    }

    class Inventory {
        +List~Product~ products
        +add_product(Product : product)
        +remove_product(id)
        +update_quantity(self, id, new_quantity)
        +list_inventory(self)
        +search_product(id) Product
    }

    class Report {
        +Inventory inventory
        +generate_current_report(Document)
        +generate_historical_report(Document)
    }

    Product --* Inventory
    Inventory --* Report : "uses"
```

## Code preview:
```python
from datetime import date

class Product:
    """
    This class represents a product with attributes such as ID, name, 
    price, and quantity

    Attributes: 
        id (int): product id.
        name (str): product name.
        price (float): product price.
        quantity (int): product quantity.
        category (str): product category
        entry_date (date): Date the product entered inventory
        exit_date (date): Date the product left inventory

    Methods:
        __str__() -> str: 
            Returns product attributes.
    """
    def __init__(self, id: int, name: str, price: float, quantity: int, category: str, entry_date: date, exit_date: date = None):
        self.id = id
        self.name = name
        self.price = price
        self.quantity = quantity
        self.category = category
        self.entry_date = entry_date
        self.exit_date = exit_date

    def register_entry(self, quantity: int):
        try:
            if quantity <= 0:
                raise ValueError("Quantity must be greater than 0.")
            self.quantity += quantity
            print(f"{quantity} units of {self.name} have been added. Total in inventory: {self.quantity}.")
        except ValueError as e:
            print(f"Error: {e}")

    def register_exit(self, quantity: int):
        try:
            if quantity <= 0:
                raise ValueError("Quantity must be greater than 0.")
            if quantity > self.quantity:
                raise ValueError("Not enough units in stock.")
            self.quantity -= quantity
            print(f"{quantity} units of {self.name} have been removed. Total in inventory: {self.quantity}.")
        except ValueError as e:
            print(f"Error: {e}")

    def __str__(self):
        return (
                f"ID: {self.id}, Name: {self.name}, Price: ${self.price:.2f}, "
                f"Quantity: {self.quantity}, Category: {self.category}, "
                f"Entry Date: {self.entry_date}, Exit Date: {self.exit_date or 'N/A'}""
                )

class Inventory:
    """
    This class manages a collection of products in the inventory.

    Attributes: 

    Methods:

    """
    def __init__(self):
        self.products = []

    def add_product(self, product):
        if product.id in self.products:
            print("The product already exists in the inventory.")
        else:
            self.products[product.id] = product
            print("Product added successfully.")

    def remove_product(self, id):
        if id in self.products:
            del self.products[id]
            print("Product removed successfully.")
        else:
            print("The product does not exist in the inventory.")

    def update_quantity(self, id, new_quantity):
        if id in self.products:
            self.products[id].quantity = new_quantity
            print("Quantity updated successfully.")
        else:
            print("Product with ID {id} not found.")

    def list_products(self):
        print("\nCurrent Inventory:")
        if not self.products:
            print("The inventory is empty.")
        else:
            for product in self.products.values():
                print(product.__str__())
    def search_product(self, id: int):
        for product in self.products:
            if product.id == id:
                return product
        print(f"Product with ID {id} not found.")
        return None


def start_program():
    inventory = Inventory()
    while True:
        print("\nInventory Management")
        print("1. Add product")
        print("2. Remove product")
        print("3. Update product quantity")
        print("4. List products")
        print("5. Exit")
        option = input("Select an option: ")

        if option == "1":
            product_id = int(input("Enter the product ID: "))
            name = input("Enter the product name: ")
            price = float(input("Enter the product price: "))
            quantity = int(input("Enter the product quantity: "))
            product = Product(id, name, price, quantity)
            inventory.add_product(product)

        elif option == "2":
            product_id = int(input("Enter the product ID to remove: "))
            inventory.remove_product(product_id)

        elif option == "3":
            product_id = int(input("Enter the product ID to update: "))
            new_quantity = int(input("Enter the new quantity: "))
            inventory.update_quantity(id, new_quantity)

        elif option == "4":
            inventory.list_products()

        elif option == "5":
            print("Exiting the program")
            break

        else:
            print("Invalid option. Please try again.") 
if __name__ == "__main__":  
    start_program()
```



