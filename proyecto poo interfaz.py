import csv
import os
import threading
from datetime import date
from tkinter import *
from tkinter import ttk, messagebox


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
            messagebox.showinfo("Entry Registered", f"{quantity} units of {self.name} have been added. Total in inventory: {self.quantity}.")
        except (ValueError, TypeError) as e:
            messagebox.showerror("Error", f"Error: {e}")

    def register_exit(self, quantity: int):
        try:
            if quantity <= 0:
                raise ValueError("Quantity must be greater than 0.")
            if quantity > self.quantity:
                raise ValueError("Not enough units in stock.")
            self.quantity -= quantity
            messagebox.showinfo("Exit Registered", f"{quantity} units of {self.name} have been removed. Total in inventory: {self.quantity}.")
        except (ValueError, TypeError) as e:
            messagebox.showerror("Error", f"Error: {e}")

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
            messagebox.showwarning("Warning", "The product already exists in the inventory.")
        else:
            self.products.append(product)
            messagebox.showinfo("Product Added", f"Product {product.name} successfully added to inventory.")

    def remove_product(self, id: int):
        product = self.search_product(id)
        if product:
            self.products.remove(product)
            messagebox.showinfo("Product Removed", f"Product {product.name} removed successfully from inventory.")
        else:
            messagebox.showerror("Error", f"Product with ID {id} not found.")

    def list_inventory(self):
        inventory_list = "\n=== Current Inventory ===\n"
        if not self.products:
            inventory_list += "The inventory is empty."
        for product in self.products:
            inventory_list += f"{product}\n"
        return inventory_list

    def search_product(self, id: int):
        for product in self.products:
            if product.id == id:
                return product
        return None

    def update_quantity(self, id: int, new_quantity: int):
        try:
            product = self.search_product(id)
            if product is None:
                raise ValueError(f"Product with ID {id} not found.")  # Exception if the ID doesn't exists

            if not isinstance(new_quantity, int):
                raise TypeError("Quantity must be an integer.")  # Exception is the quantity is not an integer

            if new_quantity < 0:
                raise ValueError("Quantity cannot be negative.")  # Exception if new_quantity is negative

            product.quantity = new_quantity
            messagebox.showinfo("Quantity Updated", f"Successfully updated quantity of {product.name} to {product.quantity}.\n")

        except (ValueError, TypeError) as e:
            messagebox.showerror("Error", f"Error in update_quantity: {e}\n")

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
        messagebox.showinfo("Success", f"Inventory saved to {filename} successfully.")

    def load_from_csv(self, filename: str = "inventory.csv"):
        # Loads products and information from a CSV file into the current inventory.
        # Limpiamos la lista para "reconstruir" el inventario
        self.products.clear()

        # Verificamos si el archivo existe
        if not os.path.exists(filename):
            messagebox.showwarning("Warning", f"File '{filename}' does not exist. Starting with an empty inventory.")
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

        messagebox.showinfo("Success", f"Inventory loaded from {filename} successfully.")


class Report:
    # Class that manages reports of inventory
    def __init__(self, inventory: Inventory):
        self.inventory = inventory

    def _generate_report_logic(self):
        # Internal method to generate the report without blocking the main thread.
        report = self.inventory.list_inventory()
        messagebox.showinfo("Current Inventory Report", report)

    def generate_current_report(self):
        # Generates a report of the current inventory on a separated thread
        thread = threading.Thread(target=self._generate_report_logic)
        thread.start()

    def generate_historical_report(self):
        # Generates an historical report of inventory
        historical_report = "Historical Inventory Report:\n"
        for product in self.inventory.products:
            historical_report += (f"Product: {product.name}, Entry Date: {product.entry_date}, "
                                  f"Exit Date: {product.exit_date or 'N/A'}\n")
        messagebox.showinfo("Historical Inventory Report", historical_report)


class InventoryGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Inventory Management")
        self.inventory = Inventory()

        # Create the notebook
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(expand=1, fill='both')

        # Add tabs
        self.create_add_product_tab()
        self.create_remove_product_tab()
        self.create_list_products_tab()
        self.create_search_product_tab()
        self.create_update_quantity_tab()
        self.create_register_entry_exit_tab()
        self.create_csv_tab()

    def create_add_product_tab(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Add Product")

        Label(frame, text="Product ID:").grid(row=0, column=0, padx=10, pady=5)
        self.add_product_id = Entry(frame)
        self.add_product_id.grid(row=0, column=1, padx=10, pady=5)

        Label(frame, text="Product Name:").grid(row=1, column=0, padx=10, pady=5)
        self.add_product_name = Entry(frame)
        self.add_product_name.grid(row=1, column=1, padx=10, pady=5)

        Label(frame, text="Product Price:").grid(row=2, column=0, padx=10, pady=5)
        self.add_product_price = Entry(frame)
        self.add_product_price.grid(row=2, column=1, padx=10, pady=5)

        Label(frame, text="Product Quantity:").grid(row=3, column=0, padx=10, pady=5)
        self.add_product_quantity = Entry(frame)
        self.add_product_quantity.grid(row=3, column=1, padx=10, pady=5)

        Label(frame, text="Product Category:").grid(row=4, column=0, padx=10, pady=5)
        self.add_product_category = Entry(frame)
        self.add_product_category.grid(row=4, column=1, padx=10, pady=5)

        Label(frame, text="Entry Date (YYYY-MM-DD):").grid(row=5, column=0, padx=10, pady=5)
        self.add_product_entry_date = Entry(frame)
        self.add_product_entry_date.grid(row=5, column=1, padx=10, pady=5)

        Button(frame, text="Add Product", command=self.add_product).grid(row=6, column=0, columnspan=2, pady=10)

    def create_remove_product_tab(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Remove Product")

        Label(frame, text="Product ID to Remove:").grid(row=0, column=0, padx=10, pady=5)
        self.remove_product_id = Entry(frame)
        self.remove_product_id.grid(row=0, column=1, padx=10, pady=5)

        Button(frame, text="Remove Product", command=self.remove_product).grid(row=1, column=0, columnspan=2, pady=10)

    def create_list_products_tab(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="List Products")

        Button(frame, text="List Products", command=self.list_products).pack(pady=10)

        self.list_products_text = Text(frame, wrap=WORD, width=60, height=20)
        self.list_products_text.pack(pady=10)

    def create_search_product_tab(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Search Product")

        Label(frame, text="Product ID to Search:").grid(row=0, column=0, padx=10, pady=5)
        self.search_product_id = Entry(frame)
        self.search_product_id.grid(row=0, column=1, padx=10, pady=5)

        Button(frame, text="Search Product", command=self.search_product).grid(row=1, column=0, columnspan=2, pady=10)

        self.search_product_text = Text(frame, wrap=WORD, width=60, height=20)
        self.search_product_text.grid(row=2, column=0, columnspan=2, pady=10)

    def create_update_quantity_tab(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Update Quantity")

        Label(frame, text="Product ID to Update:").grid(row=0, column=0, padx=10, pady=5)
        self.update_quantity_id = Entry(frame)
        self.update_quantity_id.grid(row=0, column=1, padx=10, pady=5)

        Label(frame, text="New Quantity:").grid(row=1, column=0, padx=10, pady=5)
        self.update_quantity_value = Entry(frame)
        self.update_quantity_value.grid(row=1, column=1, padx=10, pady=5)

        Button(frame, text="Update Quantity", command=self.update_quantity).grid(row=2, column=0, columnspan=2, pady=10)

    def create_register_entry_exit_tab(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Register Entry/Exit")

        Label(frame, text="Product ID:").grid(row=0, column=0, padx=10, pady=5)
        self.entry_exit_product_id = Entry(frame)
        self.entry_exit_product_id.grid(row=0, column=1, padx=10, pady=5)

        Label(frame, text="Quantity:").grid(row=1, column=0, padx=10, pady=5)
        self.entry_exit_quantity = Entry(frame)
        self.entry_exit_quantity.grid(row=1, column=1, padx=10, pady=5)

        Button(frame, text="Register Entry", command=self.register_entry).grid(row=2, column=0, columnspan=2, pady=10)
        Button(frame, text="Register Exit", command=self.register_exit).grid(row=3, column=0, columnspan=2, pady=10)

    def create_csv_tab(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="CSV Operations")

        Label(frame, text="CSV Filename (default: 'inventory.csv'):").grid(row=0, column=0, padx=10, pady=5)
        self.csv_filename = Entry(frame)
        self.csv_filename.grid(row=0, column=1, padx=10, pady=5)
        self.csv_filename.insert(0, "inventory.csv")

        Button(frame, text="Save to CSV", command=self.save_to_csv).grid(row=1, column=0, columnspan=2, pady=10)
        Button(frame, text="Load from CSV", command=self.load_from_csv).grid(row=2, column=0, columnspan=2, pady=10)

    def add_product(self):
        try:
            id = int(self.add_product_id.get())
            name = self.add_product_name.get()
            price = float(self.add_product_price.get())
            quantity = int(self.add_product_quantity.get())
            category = self.add_product_category.get()
            entry_date_str = self.add_product_entry_date.get()
            entry_date = date.fromisoformat(entry_date_str) if entry_date_str else date.today()
            product = Product(id, name, price, quantity, category, entry_date)
            self.inventory.add_product(product)
        except ValueError as e:
            messagebox.showerror("Error", f"Invalid input: {e}")

    def remove_product(self):
        try:
            id = int(self.remove_product_id.get())
            self.inventory.remove_product(id)
        except ValueError as e:
            messagebox.showerror("Error", f"Invalid input: {e}")

    def list_products(self):
        self.list_products_text.delete(1.0, END)
        inventory_list = self.inventory.list_inventory()
        self.list_products_text.insert(END, inventory_list)

    def search_product(self):
        try:
            id = int(self.search_product_id.get())
            product = self.inventory.search_product(id)
            if product:
                self.search_product_text.delete(1.0, END)
                self.search_product_text.insert(END, str(product))
            else:
                messagebox.showinfo("Not Found", f"Product with ID {id} not found.")
        except ValueError as e:
            messagebox.showerror("Error", f"Invalid input: {e}")

    def update_quantity(self):
        try:
            id = int(self.update_quantity_id.get())
            new_quantity = int(self.update_quantity_value.get())
            self.inventory.update_quantity(id, new_quantity)
        except ValueError as e:
            messagebox.showerror("Error", f"Invalid input: {e}")

    def register_entry(self):
        try:
            id = int(self.entry_exit_product_id.get())
            quantity = int(self.entry_exit_quantity.get())
            product = self.inventory.search_product(id)
            if product:
                product.register_entry(quantity)
            else:
                messagebox.showinfo("Not Found", f"Product with ID {id} not found.")
        except ValueError as e:
            messagebox.showerror("Error", f"Invalid input: {e}")

    def register_exit(self):
        try:
            id = int(self.entry_exit_product_id.get())
            quantity = int(self.entry_exit_quantity.get())
            product = self.inventory.search_product(id)
            if product:
                product.register_exit(quantity)
            else:
                messagebox.showinfo("Not Found", f"Product with ID {id} not found.")
        except ValueError as e:
            messagebox.showerror("Error", f"Invalid input: {e}")

    def save_to_csv(self):
        filename = self.csv_filename.get()
        self.inventory.save_to_csv(filename)

    def load_from_csv(self):
        filename = self.csv_filename.get()
        self.inventory.load_from_csv(filename)


if __name__ == "__main__":
    root = Tk()
    app = InventoryGUI(root)
    root.mainloop()