
def particion(lista, inicio, fin):
    """Coloca el pivote en su posición final y regresa esa posición.
    Los menores quedan a su izquierda y los mayores a su derecha."""
    
    medio = (inicio + fin) // 2
    lista[medio], lista[fin] = lista[fin], lista[medio]
    pivote = lista[fin]

    indice = inicio                   
    for j in range(inicio, fin):
        if lista[j] < pivote:        
            lista[indice], lista[j] = lista[j], lista[indice]
            indice += 1
    
    lista[indice], lista[fin] = lista[fin], lista[indice]
    return indice


def quick_sort(lista, inicio, fin):
    """Ordena lista[inicio..fin] de forma recursiva."""
    if inicio < fin:                
        posicion_pivote = particion(lista, inicio, fin)
        quick_sort(lista, inicio, posicion_pivote - 1)   
        quick_sort(lista, posicion_pivote + 1, fin)     
    return lista


def pedir_cantidad():
    """Pide la cantidad de números; valida que sea entero positivo."""
    while True:
        texto = input("¿Cuántos números desea ingresar? ")
        try:
            cantidad = int(texto)
            if cantidad > 0:
                return cantidad
            print("Error: la cantidad debe ser un entero positivo (mayor que 0).")
        except ValueError:
            print("Error: debe escribir un número entero.")


def pedir_numeros(cantidad):
    """Captura los números uno por uno; valida que sean enteros."""
    numeros = []
    for i in range(cantidad):
        while True:
            texto = input(f"Número {i + 1} de {cantidad}: ")
            try:
                numeros.append(int(texto))
                break
            except ValueError:
                print("Error: debe escribir un número entero.")
    return numeros


def ordenar_numeros():
    """Realiza todo el procedimiento: captura, ordena y muestra."""
    cantidad = pedir_cantidad()
    numeros = pedir_numeros(cantidad)
    print("\nLista original:", numeros)
    copia = numeros[:]                
    ordenada = quick_sort(copia, 0, len(copia) - 1)
    print("Lista ordenada (menor a mayor):", ordenada)


def menu():
    """Menú principal: se repite hasta que el usuario elija salir."""
    while True:
        print("\n===== ORDENAMIENTO QUICKSORT =====")
        print("1. Ordenar números")
        print("2. Salir")
        opcion = input("Seleccione una opción: ").strip()
        if opcion == "1":
            ordenar_numeros()
        elif opcion == "2":
            print("Programa finalizado.")
            break
        else:
            print("Opción no válida. Intente de nuevo.")


if __name__ == "__main__":
    menu()