cantidad = int(input("¿Cuántos números deseas ordenar? "))
lista = []

for i in range(cantidad):
    numero = int(input("Ingresa el número " + str(i + 1) + ": "))
    lista.append(numero)


print("\nLista original:", lista)


tamano = len(lista)

for pasada in range(tamano - 1):
    for posicion in range(tamano - 1 - pasada):
       
        if lista[posicion] > lista[posicion + 1]:
            auxiliar = lista[posicion]
            lista[posicion] = lista[posicion + 1]
            lista[posicion + 1] = auxiliar

print("Lista ordenada:", lista)