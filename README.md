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
class Product:
    """
    This class represents a product with attributes such as ID, name, 
    price, and quantity

    Attributes: 
        product_id (int): product id.
        name (str): product name.
        price (float): product price.
        quantity (int): product quantity.

    Methods:
        product_details() -> str: 
            Returns product attributes.
    """
    def __init__(self, product_id, name, price, quantity):
        self.product_id = product_id
        self.name = name
        self.price = price
        self.quantity = quantity
        
    def product_details(self):
        return (
            f"ID: {self.product_id}, Name: {self.name}, Price: {self.price}, "
            f"Quantity: {self.quantity}"
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



