from MyLinkedList import ListaEnlazada, CicloError

print("Importé la biblioteca y NO se abrió ningún menú.")

lista = ListaEnlazada()
lista.insertar_final("A")
lista.insertar_final("B")
lista.insertar_final("C")
print("Principal:", lista.datos())

lista.crear_rama(lista.buscar("C"), "X")
print(lista.a_texto())

try:
    lista.enlazar(lista.buscar("C"), lista.buscar("A"))
except CicloError:
    print("Ciclo rechazado correctamente")