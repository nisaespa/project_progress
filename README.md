# Warehouse Inventory System


## Flow charts:

``` mermaid
classDiagram
    class Product {
        + product_id : int
        + name : string
        + price : float
        + quantity : int
        + category : string
        + entry_date : date
        + exit_date : date
        +register_entry(quantity : int)
        +register_exit(quantity : int)
        +__str __()
    }

    class Inventory {
        +List~Product~ products
        +add_product(Product : product)
        +remove_product(id : int)
        +list_inventory()
        +search_product(id : int) Product
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
        product_id (int): product id.
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
    def __init__(self, product_id: int, name: str, price: float, quantity: int, category: str, entry_date: date):
        self.product_id = product_id
        self.name = name
        self.price = price
        self.quantity = quantity
        self.category = category
        self.entry_date = entry_date

    def __str__(self):
        return (
                f"ID: {self.product_id}, Name: {self.name}, Price: ${self.price:.2f}, "
                f"Quantity: {self.quantity}, Category: {self.category}, "
                f"Entry Date: {self.entry_date}"
                )
    

class Inventory:
    """
    This class manages a collection of products in the inventory.

    Attributes: 

    Methods:

    """
    def __init__(self):
        self.products = {}

    def add_product(self, product):
        if product.product_id in self.products:
            print("The product already exists in the inventory.")
        else:
            self.products[product.product_id] = product
            print("Product added successfully.")

    def remove_product(self, product_id):
        if product_id in self.products:
            del self.products[product_id]
            print("Product removed successfully.")
        else:
            print("The product does not exist in the inventory.")

    def update_quantity(self, product_id, new_quantity):
        if product_id in self.products:
            self.products[product_id].quantity = new_quantity
            print("Quantity updated successfully.")
        else:
            print("The product does not exist in the inventory.")

    def register_entry(self, product_id, quantity):
        # Increase quantity of product in the inventory
        if product_id in self.products:
            self.products[product_id].quantity += quantity
            print(f"{quantity} units of {self.name} have been added. Total in inventory: {self.quantity}.")
        else:
            print("The product does not exist in the inventory.")
       
    def register_exit(self, product_id, quantity):
        # Reduce quantity of product in the inventory
        if product_id in self.products:
            if quantity > self.quantity:
                print(f"Not enough units of {self.name} to remove {quantity} units.")
            else:
                self.products[product_id].quantity -= quantity
                print(f"{quantity} units of {self.name} have been removed. Total in inventory: {self.quantity}.")
                print("Quantity updated successfully.")
        else:
            print("The product does not exist in the inventory.")

    def list_products(self):
        if not self.products:
            print("The inventory is empty.")
        else:
            for product in self.products.values():
                print(product.product_details())


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
            product = Product(product_id, name, price, quantity)
            inventory.add_product(product)

        elif option == "2":
            product_id = int(input("Enter the product ID to remove: "))
            inventory.remove_product(product_id)

        elif option == "3":
            product_id = int(input("Enter the product ID to update: "))
            new_quantity = int(input("Enter the new quantity: "))
            inventory.update_quantity(product_id, new_quantity)

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



