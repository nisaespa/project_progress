# <div align='center'> Warehouse Inventory System 📝 </div>

## <div align='center'> ✧ Team Rocket ✧ </div>
<div align='center'>
<figure> <img src="https://raw.githubusercontent.com/nisaespa/project_progress/refs/heads/main/TeamRocket.png" alt="" width="450" height="auto"/></br>
<figcaption><b></b></figcaption></figure>
</div>

### Description

We are developing an inventory manager with the acquired knowledge across this semester in order to get a useful program.
The code is pretty basic at the moment, nowadays its useful, it uses two principal classes, Inventory and Product.
Inventory is composed by product; so Product is used to create the information of each product that is stored in the Inventory, and the metods for printing a string with a product characteristics, adding or removing a determinated quantity to an already created product, then we have the class Inventory that generates a list of the products and has metods that lets update the amount of a product, adding or removing products, printing the str of all the products contained on Inventory, and two static methods that are used for clearing the screen directly or pausing the execution of the program until the user presses Enter.  

## UML Class Diagrams:
``` mermaid
classDiagram
    class Product {
        + id : int
        + name : string
        # price : float
        + quantity : int
        + category : string
        + entry_date : date
        + exit_date : date
        + register_entry(quantity : int)
        + register_exit(quantity : int)
        # get_price() : float
        # set_price(value : float) : Bool
        + __str __()
    }

    class Inventory {
        + products : List~Product~ 
        + add_product(product : Product)
        + remove_product(id, product : Product)
        + update_quantity(id, new_quantity : float)
        + list_products()
        + search_product(product : Product)
        + save_to_csv(filename: str = "inventory.csv")
        + load_from_csv(filename: str = "inventory.csv")
        + @clear_screen()
        + @pause()
    }

    class Report {
        + inventory : Inventory
        + _generate_report_logic()
        + generate_current_report() Document
        + generate_historical_report() Document
    }

    Product --* Inventory
    Inventory --* Report : generates
```

## Code preview:
```python
import csv
import os
import threading
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
        register_entry(self, quantity):
            For increasing product quantity
        register_exit(self, quantity):
            For reducing product quantity
        get_price(self):
            Getter that returns product price
        set_price(self, value) -> float:
            Setter for product price
    """
    def __init__(self, id: int, name: str, price: float, quantity: int, category: str, entry_date: date, exit_date: date = None):
        self.id = id
        self.name = name
        self._price = price
        self.quantity = quantity
        self.category = category
        self.entry_date = entry_date
        self.exit_date = exit_date

    def register_entry(self, quantity: int):
        try:
            if quantity <= 0:
                raise ValueError("Quantity must be greater than 0.")
            self.quantity += quantity
            print(f"\n{quantity} units of {self.name} have been added. Total in inventory: {self.quantity}.")
        except (ValueError, TypeError) as e:
            print(f"Error: {e}")

    def register_exit(self, quantity: int):
        try:
            if quantity <= 0:
                raise ValueError("Quantity must be greater than 0.")
            if quantity > self.quantity:
                raise ValueError("Not enough units in stock.")
            self.quantity -= quantity
            print(f"\n{quantity} units of {self.name} have been removed. Total in inventory: {self.quantity}.")
        except (ValueError, TypeError) as e:
            print(f"Error: {e}")

    def get_price(self):
        return self._price

    def set_price(self, value: float):
        if value <= 0:
            raise ValueError("Price must be greater than 0.")
        self._price = value


    def __str__(self):
        exit_date_str = self.exit_date if self.exit_date else "N/A"
        return (
                f"ID: {self.id}, Name: {self.name}, Price: ${self._price:.2f}, "
                f"Quantity: {self.quantity}, Category: {self.category}, "
                f"Entry Date: {self.entry_date}, Exit Date: {exit_date_str}"
                )

class Inventory:
    """
    This class manages a collection of products in the inventory.

    Attributes: self, generates a list of products

    Methods:
        add_product(self, product: Product):
            Adds a new product to the inventory if its ID is not already in use.
        remove_product(self, product_id: int):
            Removes a product from the inventory by its ID, if found.
        list_inventory(self):
            Displays all current products in the inventory.
        search_product(self, product_id: int):
            Searches for a product by its ID and returns it if found, otherwise returns None.
        update_quantity(self, product_id: int, new_quantity: int):
            Updates the quantity of an existing product by its ID.

    """
    def __init__(self):
        self.products = []

    def add_product(self, product: Product):
        if any(p.id == product.id for p in self.products):
            print("\nThe product already exists in the inventory.")
        else:
            self.products.append(product)
            print(f"\nProduct {product.name} successfully added to inventory.")

    def remove_product(self, id: int):
        product = self.search_product(id)
        if product:
            self.products.remove(product)
            print(f"\nProduct {product.name} removed successfully from inventory.")
        else:
            print(f"\nProduct with ID {id} not found.")

    def list_inventory(self):
        print("\n=== Current Inventory ===")
        if not self.products:
            print("The inventory is empty.")
        for product in self.products:
            print(product)

    def search_product(self, id: int):
        for product in self.products:
            if product.id == id:
                return product
        print(f"\nProduct with ID {id} not found.")
        return None

    def update_quantity(self, id: int, new_quantity: int):
        try:
            product = self.search_product(id)
            if product is None:
                raise ValueError(f"Product with ID {id} not found.") # Exception if the ID doesn't exists

            if not isinstance(new_quantity, int):
                raise TypeError("Quantity must be an integer.") # Exception is the quantity is not an integer

            if new_quantity < 0:
                raise ValueError("Quantity cannot be negative.") # Exception if new_quantity is negative
            
            product.quantity = new_quantity
            print(f"Successfully updated quantity of {product.name} to {product.quantity}.\n")

        except (ValueError, TypeError) as e:
            print(f"Error in update_quantity: {e}\n")

    # -----------------------------
    # Métodos para CSV
    # -----------------------------
    def save_to_csv(self, filename: str = "inventory.csv"):
        # Saves the current inventory to a CSV file.
        with open(filename, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            # Encabezado
            writer.writerow(["id", "name", "price", "quantity", "category", "entry_date", "exit_date"])
            # Datos de cada producto
            for product in self.products:
                entry_date_str = product.entry_date.isoformat()
                exit_date_str = product.exit_date.isoformat() if product.exit_date else ""
                writer.writerow([
                    product.id,
                    product.name,
                    product._price,
                    product.quantity,
                    product.category,
                    entry_date_str,
                    exit_date_str
                ])
        print(f"\nInventory saved to {filename} successfully.")

    def load_from_csv(self, filename: str = "inventory.csv"):
        # Loads products and information from a CSV file into the current inventory.
        # Limpiamos la lista para "reconstruir" el inventario
        self.products.clear()

        # Verificamos si el archivo existe
        if not os.path.exists(filename):
            print(f"\nFile '{filename}' does not exist. Starting with an empty inventory.")
            return

        with open(filename, mode="r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                product_id = int(row["id"])
                name = row["name"]
                price = float(row["price"])
                quantity = int(row["quantity"])
                category = row["category"]
                
                # Convertir string a date usando isoformat
                entry_date_str = row["entry_date"]
                exit_date_str = row["exit_date"]

                entry_date = date.fromisoformat(entry_date_str) if entry_date_str else None
                exit_date = date.fromisoformat(exit_date_str) if exit_date_str else None

                new_product = Product(
                    id=product_id,
                    name=name,
                    price=price,
                    quantity=quantity,
                    category=category,
                    entry_date=entry_date,
                    exit_date=exit_date
                )
                self.products.append(new_product)

        print(f"\nInventory loaded from {filename} successfully.")


    @staticmethod
    def clear_screen():
        """Clears the console"""
        os.system("cls" if os.name == "nt" else "clear")

    @staticmethod
    def pause():
        """Pauses execution until user inputs Enter."""
        input("\nPress Enter to continue ...")
        Inventory.clear_screen()

class Report:
# Class that manages reports of inventory
    def __init__(self, inventory: Inventory):
        self.inventory = inventory

    def _generate_report_logic(self):
        # Internal method to generate the report without blocking the main thread.
        self.inventory.list_inventory()

    def generate_current_report(self):
        # Generates a report of the current inventory on a separated thread
        print("Generating Current Inventory Report in background...\n")
        thread = threading.Thread(target=self._generate_report_logic)
        thread.start()

    def generate_historical_report(self):
        # Generates an historical report of inventory
        print("Historical Inventory Report:")
        for product in self.inventory.products:
            print(f"Product: {product.name}, Entry Date: {product.entry_date}, "
                  f"Exit Date: {product.exit_date or 'N/A'}")

def main():
    inventory = Inventory()
    while True:
        print("\nInventory Management\n")
        print("1. Add product")
        print("2. Remove product")
        print("3. List products")
        print("4. Search product with ID")
        print("5. Update product quantity")
        print("6. Register product ENTRY")
        print("7. Register product EXIT")        
        print("8. Save inventory to CSV")
        print("9. Load inventory from CSV")
        print("10. Exit")
        option = input("\nSelect an option: ")

        if option == "1":
            id = int(input("Enter the product ID: "))
            name = input("Enter the product name: ")
            price = float(input("Enter the product price: "))
            quantity = int(input("Enter the product quantity: "))
            category = input("Enter the product category: ")
            entry_date = input("Enter the date the product entered inventory (Format: YYYY, MM, DD), for today's date just press Enter): ")
            try:
                year_str, month_str, day_str = entry_date.split(",")
                year = int(year_str.strip())
                month = int(month_str.strip())
                day = int(day_str.strip())
                entry_date = date(year, month, day)
            except (ValueError, TypeError):
                print("\nInvalid date format. Today's date will be used")
                entry_date = date.today()
            product = Product(id, name, price, quantity, category, entry_date)
            inventory.add_product(product)
            Inventory.pause()

        elif option == "2":
            id = int(input("Enter the product ID to remove: "))
            inventory.remove_product(id)
            Inventory.pause()

        elif option == "3":
            inventory.list_inventory()
            Inventory.pause()

        elif option == "4":
            id = int(input("Enter the product ID to search: "))        
            inventory.search_product(id)
            if product:
                print(product)
            else:
                print(f"\nProduct with ID {id} not found.")
            Inventory.pause()

        elif option == "5":
            id = int(input("Enter the product ID to update: "))
            new_quantity = int(input("Enter the new quantity: "))
            inventory.update_quantity(id, new_quantity)   
            Inventory.pause()

        elif option == "6":
            id = int(input("Enter the product ID to register ENTRY: "))
            quantity_to_add = int(input("Enter the quantity to add: "))
            product_found = inventory.search_product(id)
            if product_found:
                product.register_entry(quantity_to_add)
            else:
                print(f"\nProduct with ID {id} not found.")
            Inventory.pause()

        elif option == "7":
            id = int(input("Enter the product ID to register EXIT: "))
            quantity_to_remove = int(input("Enter the quantity to remove: "))
            product_found = inventory.search_product(id)
            if product_found:
                product.register_exit(quantity_to_remove)
            else:
                print(f"\nProduct with ID {id} not found.")
            Inventory.pause()

        elif option == "8":
            filename = input("Enter the CSV filename (default: 'inventory.csv'): ")
            filename = filename.strip() if filename else "inventory.csv"
            inventory.save_to_csv(filename)
            Inventory.pause()

        elif option == "9":
            filename = input("Enter the CSV filename (default: 'inventory.csv'): ")
            filename = filename.strip() if filename else "inventory.csv"
            inventory.load_from_csv(filename)
            Inventory.pause()

        elif option == "10":
            print("\nInventory closed succesfully")
            break

        else:
            print("\nInvalid option. Please try again.")
            Inventory.pause()

if __name__ == "__main__":  
    main()
```




