# Sistema de inventario de una bodega

```python
class Producto:
    def __init__(self, id_producto, nombre, precio, cantidad):
        self.id_producto = id_producto
        self.nombre = nombre
        self.precio = precio
        self.cantidad = cantidad

    def detalles_producto(self):
        return f"ID: {self.id_producto}, Nombre: {self.nombre}, Precio: {self.precio}, Cantidad: {self.cantidad}"

class Inventario:
    def __init__(self):
        self.productos = {}

    def agregar_producto(self, producto):
        if producto.id_producto in self.productos:
            print("El producto ya existe en el inventario.")
        else:
            self.productos[producto.id_producto] = producto
            print("Producto agregado correctamente.")

    def eliminar_producto(self, id_producto):
        if id_producto in self.productos:
            del self.productos[id_producto]
            print("Producto eliminado correctamente.")
        else:
            print("El producto no existe en el inventario.")

    def actualizar_cantidad(self, id_producto, nueva_cantidad):
        if id_producto in self.productos:
            self.productos[id_producto].cantidad = nueva_cantidad
            print("Cantidad actualizada correctamente.")
        else:
            print("El producto no existe en el inventario.")

    def listar_productos(self):
        if not self.productos:
            print("El inventario está vacío.")
        else:
            for producto in self.productos.values():
                print(producto.detalles_producto())

# Ejemplo de uso
if __name__ == "__main__":
    inventario = Inventario()

    while True:
        print("\nGestión de Inventario")
        print("1. Agregar producto")
        print("2. Eliminar producto")
        print("3. Actualizar cantidad de producto")
        print("4. Listar productos")
        print("5. Salir")
        opcion = input("Selecciona una opción: ")

        if opcion == "1":
            id_producto = int(input("Ingresa el ID del producto: "))
            nombre = input("Ingresa el nombre del producto: ")
            precio = float(input("Ingresa el precio del producto: "))
            cantidad = int(input("Ingresa la cantidad del producto: "))
            producto = Producto(id_producto, nombre, precio, cantidad)
            inventario.agregar_producto(producto)

        elif opcion == "2":
            id_producto = int(input("Ingresa el ID del producto a eliminar: "))
            inventario.eliminar_producto(id_producto)

        elif opcion == "3":
            id_producto = int(input("Ingresa el ID del producto a actualizar: "))
            nueva_cantidad = int(input("Ingresa la nueva cantidad: "))
            inventario.actualizar_cantidad(id_producto, nueva_cantidad)

        elif opcion == "4":
            inventario.listar_productos()

        elif opcion == "5":
            print("Saliendo del programa...")
            break

        else:
            print("Opción no válida. Intenta nuevamente.")
```



