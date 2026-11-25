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


if __name__ == "__main__":
    ejecutar_hash()
