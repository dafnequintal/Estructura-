
cantidad = int(input("¿Cuántos números deseas ordenar? "))
lista = []

for i in range(cantidad):
    numero = int(input("Ingresa el número " + str(i + 1) + ": "))
    lista.append(numero)


print("\nLista original:", lista)


tamano = len(lista)

for i in range(tamano - 1):
    posicion_menor = i  
    
    for j in range(i + 1, tamano):
        if lista[j] < lista[posicion_menor]:
            posicion_menor = j

   
    if posicion_menor != i:
        auxiliar = lista[i]
        lista[i] = lista[posicion_menor]
        lista[posicion_menor] = auxiliar


print("Lista ordenada:", lista)