
def radix_positivos(lista):
    """Radix Sort (LSD) para números enteros mayores o iguales a 0.
    Ordena dígito por dígito: unidades, decenas, centenas, etc."""
    if len(lista) == 0:
        return lista

    maximo = max(lista)              
    exp = 1                           

    while maximo // exp > 0:
        
        cubetas = [[] for _ in range(10)]
        for numero in lista:
            digito = (numero // exp) % 10
            cubetas[digito].append(numero)   

       
        lista = []
        for cubeta in cubetas:
            lista.extend(cubeta)
        exp *= 10                    
    return lista


def radix_sort(lista):
    """Radix Sort para enteros positivos, negativos y repetidos."""
    
    negativos = []
    positivos = []
    for numero in lista:
        if numero < 0:
            negativos.append(-numero)    
        else:
            positivos.append(numero)

    negativos = radix_positivos(negativos)
    positivos = radix_positivos(positivos)

  
    resultado = []
    for i in range(len(negativos) - 1, -1, -1):
        resultado.append(-negativos[i])
    resultado.extend(positivos)
    return resultado


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
    ordenada = radix_sort(numeros)
    print("Lista ordenada (menor a mayor):", ordenada)


def menu():
    """Menú principal: se repite hasta que el usuario elija salir."""
    while True:
        print("\n===== ORDENAMIENTO RADIX SORT =====")
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