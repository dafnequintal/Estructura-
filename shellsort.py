
def shell_sort(lista):
    """Ordena la lista de menor a mayor con ShellSort y la regresa."""
    n = len(lista)
    gap = n // 2                     
    while gap > 0:                   
        for i in range(gap, n):
            temporal = lista[i]     
            j = i
           
            while j >= gap and lista[j - gap] > temporal:
                lista[j] = lista[j - gap]
                j -= gap
            lista[j] = temporal       
        gap //= 2                     
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
    ordenada = shell_sort(numeros[:])  
    print("Lista ordenada (menor a mayor):", ordenada)


def menu():
    """Menú principal: se repite hasta que el usuario elija salir."""
    while True:
        print("\n===== ORDENAMIENTO SHELLSORT =====")
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