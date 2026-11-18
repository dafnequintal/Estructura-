
def heapify(lista, tamano, raiz):
    """Acomoda el nodo 'raiz' para que cumpla la regla del Max Heap:
    todo padre debe ser mayor o igual que sus hijos."""
    mayor = raiz
    hijo_izq = 2 * raiz + 1          
    hijo_der = 2 * raiz + 2           

    if hijo_izq < tamano and lista[hijo_izq] > lista[mayor]:
        mayor = hijo_izq
    if hijo_der < tamano and lista[hijo_der] > lista[mayor]:
        mayor = hijo_der

    if mayor != raiz:                
        lista[raiz], lista[mayor] = lista[mayor], lista[raiz]
        heapify(lista, tamano, mayor)


def heap_sort(lista):
    """Ordena la lista de menor a mayor con Heapsort y la regresa."""
    n = len(lista)

    
    for i in range(n // 2 - 1, -1, -1):
        heapify(lista, n, i)

    
    for fin in range(n - 1, 0, -1):
        lista[0], lista[fin] = lista[fin], lista[0]  
        heapify(lista, fin, 0)        
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
    ordenada = heap_sort(numeros[:])  
    print("Lista ordenada (menor a mayor):", ordenada)


def menu():
    """Menú principal: se repite hasta que el usuario elija salir."""
    while True:
        print("\n===== ORDENAMIENTO HEAPSORT =====")
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