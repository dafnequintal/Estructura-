def busqueda_binaria(productos, codigo_buscado):
    """Busca el código en la lista ordenada, dividiéndola a la mitad en cada paso.
    Cada producto es una tupla (codigo, nombre, precio).
    Regresa la posición (o -1 si no existe) y el número de pasos."""
    izquierda = 0
    derecha = len(productos) - 1
    pasos = 0

    while izquierda <= derecha:
        pasos = pasos + 1
        medio = (izquierda + derecha) // 2
        codigo_medio = productos[medio][0]
        print(f"  Paso {pasos}: izquierda={izquierda}, derecha={derecha}, "
              f"medio={medio} (código {codigo_medio})")

        if codigo_medio == codigo_buscado:
            return medio, pasos
        elif codigo_buscado < codigo_medio:
            derecha = medio - 1     
        else:
            izquierda = medio + 1    

    return -1, pasos


def mostrar_catalogo(productos):
    print("\n--- Catálogo (ordenado por código) ---")
    for producto in productos:
        print(f"{producto[0]} | {producto[1]} | ${producto[2]:.2f}")


def ejecutar_binaria(desde_menu=False):
    
    if desde_menu:
        texto_salida = "Volver al menú principal"
    else:
        texto_salida = "Salir"

    
    catalogo = [(1002, "Cuaderno profesional", 45.00),
                (1015, "Lápiz HB", 6.50),
                (1023, "Pluma azul", 8.00),
                (1040, "Calculadora científica", 250.00),
                (1057, "Marcatextos amarillo", 15.00),
                (1068, "Regla de 30 cm", 10.00),
                (1074, "Folder tamaño carta", 5.00),
                (1090, "Tijeras escolares", 22.00),
                (1105, "Pegamento en barra", 18.00),
                (1120, "Block de hojas de colores", 30.00)]

    opcion = ""
    while opcion != "4":
        print("\n=== BÚSQUEDA BINARIA: CATÁLOGO DE PAPELERÍA ===")
        print("1. Buscar un producto por código")
        print("2. Ver el catálogo completo")
        print("3. Agregar un producto")
        print("4. " + texto_salida)
        opcion = input("Elige una opción: ")

        if opcion == "1":
            texto = input("Código del producto: ").strip()
            if not texto.isdigit():
                print("El código debe ser un número entero.")
            else:
                codigo = int(texto)
                posicion, pasos = busqueda_binaria(catalogo, codigo)
                if posicion != -1:
                    producto = catalogo[posicion]
                    print(f"Encontrado: {producto[1]}, precio ${producto[2]:.2f}")
                else:
                    print(f"El código {codigo} no existe en el catálogo.")
                print(f"Pasos realizados: {pasos}")
        elif opcion == "2":
            mostrar_catalogo(catalogo)
        elif opcion == "3":
            texto = input("Código del producto nuevo: ").strip()
            if not texto.isdigit():
                print("El código debe ser un número entero.")
            else:
                codigo = int(texto)
               
                existe, _ = busqueda_binaria(catalogo, codigo)
                if existe != -1:
                    print("Ese código ya está registrado.")
                else:
                    nombre = input("Nombre del producto: ").strip()
                    try:
                        precio = float(input("Precio: "))
                        catalogo.append((codigo, nombre, precio))
                        catalogo.sort()  
                        print("Producto agregado y catálogo reordenado.")
                    except ValueError:
                        print("El precio debe ser un número.")
        elif opcion == "4":
            if not desde_menu:
                print("Fin del programa.")
        else:
            print("Opción no válida, intenta de nuevo.")


if __name__ == "__main__":
    ejecutar_binaria()
