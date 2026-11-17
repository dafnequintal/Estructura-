cantidad = int(input("¿Cuántos números deseas ordenar? "))
lista = []

for i in range(cantidad):
    numero = int(input("Ingresa el número " + str(i + 1) + ": "))
    lista.append(numero)

print("\nLista original:", lista)

tamano = len(lista)

for i in range(1, tamano):
    valor_actual = lista[i]      
    posicion = i - 1             


    while posicion >= 0 and lista[posicion] > valor_actual:
        lista[posicion + 1] = lista[posicion]
        posicion = posicion - 1

    
    lista[posicion + 1] = valor_actual


print("Lista ordenada:", lista)