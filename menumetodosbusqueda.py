def busqueda_secuencial(lista, nombre_buscado):
    """Recorre la lista de principio a fin comparando cada nombre.
    Regresa la posición donde lo encontró (o -1 si no está)
    y cuántas comparaciones hizo."""
    comparaciones = 0
    for posicion in range(len(lista)):
        comparaciones = comparaciones + 1
        if lista[posicion].lower() == nombre_buscado.lower():
            return posicion, comparaciones
    return -1, comparaciones


def mostrar_lista(lista):
    print("\n--- Lista de asistencia ---")
    for i in range(len(lista)):
        print(f"{i + 1}. {lista[i]}")


def ejecutar_secuencial(desde_menu=False):
    if desde_menu:
        texto_salida = "Volver al menú principal"
    else:
        texto_salida = "Salir"

    # Lista inicial (sin ordenar)
    asistencia = ["Luis Pech", "María Canul", "José Chan", "Ana Cetina",
                  "Carlos May", "Daniela Uc", "Rosa Poot", "Miguel Ek"]

    opcion = ""
    while opcion != "4":
        print("\n=== BÚSQUEDA SECUENCIAL: LISTA DE ASISTENCIA ===")
        print("1. Buscar un alumno")
        print("2. Ver la lista completa")
        print("3. Agregar un alumno")
        print("4. " + texto_salida)
        opcion = input("Elige una opción: ")

        if opcion == "1":
            nombre = input("Nombre completo del alumno a buscar: ").strip()
            posicion, comparaciones = busqueda_secuencial(asistencia, nombre)
            if posicion != -1:
                print(f"Encontrado: {asistencia[posicion]} está en el lugar "
                      f"{posicion + 1} de la lista.")
            else:
                print(f"'{nombre}' no está en la lista de asistencia.")
            print(f"Comparaciones realizadas: {comparaciones}")
        elif opcion == "2":
            mostrar_lista(asistencia)
        elif opcion == "3":
            nuevo = input("Nombre del alumno nuevo: ").strip()
            if nuevo == "":
                print("No escribiste ningún nombre.")
            else:
                asistencia.append(nuevo)  
                print(f"{nuevo} se agregó al final de la lista.")
        elif opcion == "4":
            if not desde_menu:
                print("Fin del programa.")
        else:
            print("Opción no válida, intenta de nuevo.")



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


TAMANO_TABLA = 11


def calcular_hash(numero_control):
    """Función hash: el residuo de dividir entre el tamaño de la tabla
    nos da la casilla (de 0 a 10)."""
    return numero_control % TAMANO_TABLA


def crear_tabla():
    tabla = []
    for i in range(TAMANO_TABLA):
        tabla.append([])   
    return tabla


def insertar_en_tabla(tabla, numero_control, nombre, promedio):
    """Guarda un alumno. Regresa False si el número de control ya existía."""
    casilla = calcular_hash(numero_control)
    for registro in tabla[casilla]:
        if registro[0] == numero_control:
            return False
    tabla[casilla].append((numero_control, nombre, promedio))
    return True


def buscar_hash(tabla, numero_control):
    """Calcula la casilla y busca solo dentro de ella.
    Regresa el registro (o None), la casilla y las comparaciones hechas."""
    casilla = calcular_hash(numero_control)
    comparaciones = 0
    for registro in tabla[casilla]:
        comparaciones = comparaciones + 1
        if registro[0] == numero_control:
            return registro, casilla, comparaciones
    return None, casilla, comparaciones


def mostrar_tabla(tabla):
    print("\n--- Tabla hash ---")
    for casilla in range(TAMANO_TABLA):
        contenido = ""
        for registro in tabla[casilla]:
            contenido = contenido + f"[{registro[0]} {registro[1]}] "
        if contenido == "":
            contenido = "(vacía)"
        print(f"Casilla {casilla}: {contenido}")


def ejecutar_hash(desde_menu=False):
    if desde_menu:
        texto_salida = "Volver al menú principal"
    else:
        texto_salida = "Salir"

    tabla = crear_tabla()
    alumnos_iniciales = [(22080101, "Luis Pech", 92.5),
                         (22080114, "María Canul", 88.0),
                         (22080127, "José Chan", 79.4),
                         (22080133, "Ana Cetina", 95.1),
                         (22080145, "Carlos May", 84.7),
                         (22080152, "Daniela Uc", 90.3),
                         (22080168, "Rosa Poot", 76.8),
                         (22080179, "Miguel Ek", 86.0)]
    for alumno in alumnos_iniciales:
        insertar_en_tabla(tabla, alumno[0], alumno[1], alumno[2])

    opcion = ""
    while opcion != "4":
        print("\n=== BÚSQUEDA HASH: CALIFICACIONES POR NÚMERO DE CONTROL ===")
        print("1. Buscar un alumno por número de control")
        print("2. Ver la tabla hash")
        print("3. Agregar un alumno")
        print("4. " + texto_salida)
        opcion = input("Elige una opción: ")

        if opcion == "1":
            texto = input("Número de control: ").strip()
            if not texto.isdigit():
                print("El número de control debe tener solo dígitos.")
            else:
                numero = int(texto)
                registro, casilla, comparaciones = buscar_hash(tabla, numero)
                print(f"Función hash: {numero} % {TAMANO_TABLA} = casilla {casilla}")
                if registro is not None:
                    print(f"Encontrado: {registro[1]}, promedio {registro[2]}")
                else:
                    print(f"No existe ningún alumno con el número de control {numero}.")
                print(f"Comparaciones realizadas: {comparaciones}")
        elif opcion == "2":
            mostrar_tabla(tabla)
        elif opcion == "3":
            texto = input("Número de control nuevo: ").strip()
            if not texto.isdigit():
                print("El número de control debe tener solo dígitos.")
            else:
                nombre = input("Nombre del alumno: ").strip()
                try:
                    promedio = float(input("Promedio: "))
                    if insertar_en_tabla(tabla, int(texto), nombre, promedio):
                        print(f"Alumno guardado en la casilla {calcular_hash(int(texto))}.")
                    else:
                        print("Ese número de control ya está registrado.")
                except ValueError:
                    print("El promedio debe ser un número.")
        elif opcion == "4":
            if not desde_menu:
                print("Fin del programa.")
        else:
            print("Opción no válida, intenta de nuevo.")


def main():
    opcion = ""
    while opcion != "4":
        print("\n===== MÉTODOS DE BÚSQUEDA EN PYTHON =====")
        print("1. Búsqueda secuencial (lista de asistencia)")
        print("2. Búsqueda binaria (catálogo de papelería)")
        print("3. Búsqueda hash (calificaciones por número de control)")
        print("4. Salir")
        opcion = input("Elige una opción: ")

        if opcion == "1":
            ejecutar_secuencial(desde_menu=True)
        elif opcion == "2":
            ejecutar_binaria(desde_menu=True)
        elif opcion == "3":
            ejecutar_hash(desde_menu=True)
        elif opcion == "4":
            print("Programa terminado. ¡Hasta luego!")
        else:
            print("Opción no válida, intenta de nuevo.")


if __name__ == "__main__":
    main()
