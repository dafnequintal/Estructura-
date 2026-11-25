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

    
    asistencia = ["Santiago Pech", "Samanthaa Canul", "José Chan", "Valeria Cetina",
                  "Carlos Aguilar", "Dafne Quintal", "Katy Gillouard", "Miguel Sosa"]

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


if __name__ == "__main__":
    ejecutar_secuencial()
