class Nodo:
    def __init__(self, info):
        self.info = info     
        self.liga = None     




def todos_los_nodos(cabezas):
    """Devuelve todos los nodos alcanzables desde las cabezas (sin repetir)."""
    vistos, nodos = set(), []
    for cab in cabezas:
        actual = cab
        while actual is not None and id(actual) not in vistos:
            vistos.add(id(actual))
            nodos.append(actual)
            actual = actual.liga
    return nodos


def buscar(cabezas, dato):
    """Devuelve el primer nodo cuyo INFO sea igual a 'dato'."""
    for nodo in todos_los_nodos(cabezas):
        if nodo.info == dato:
            return nodo
    return None


def alcanza(desde, objetivo):
    """True si siguiendo las LIGA desde 'desde' se llega a 'objetivo'."""
    actual = desde
    while actual is not None:
        if actual is objetivo:
            return True
        actual = actual.liga
    return False


def recorrer(cabezas):
    """Muestra todas las ramas. Un * marca nodos a los que apuntan 2 o más nodos."""
    if not any(c is not None for c in cabezas):
        print("La lista está vacía (NIL)")
        return

    apuntan = {}
    for nodo in todos_los_nodos(cabezas):
        if nodo.liga is not None:
            apuntan[id(nodo.liga)] = apuntan.get(id(nodo.liga), 0) + 1

    hay_compartidos = False
    for i, cab in enumerate(cabezas):
        if cab is None:
            continue
        etiqueta = "Principal" if i == 0 else f"Rama {i}"
        actual = cab
        texto = ""
        while actual is not None:
            marca = ""
            if apuntan.get(id(actual), 0) >= 2:
                marca = "*"
                hay_compartidos = True
            texto += f"{actual.info}{marca} -> "
            actual = actual.liga
        print(f"{etiqueta}: {texto}NIL")
    if hay_compartidos:
        print("(* = nodo al que apuntan dos o más nodos)")




def insertar_inicio(P, info):
    nuevo = Nodo(info)
    nuevo.liga = P
    return nuevo


def insertar_final(P, info):
    nuevo = Nodo(info)
    if P is None:
        return nuevo
    T = P
    while T.liga is not None:
        T = T.liga
    T.liga = nuevo
    return P


def insertar_medio(P, info, posicion):
    """Inserta en la posición indicada (1 = primer lugar).
    Si la posición es mayor que el tamaño, queda al final."""
    if P is None or posicion <= 1:
        return insertar_inicio(P, info)
    nuevo = Nodo(info)
    actual = P
    for _ in range(posicion - 2):
        if actual.liga is None:
            break
        actual = actual.liga
    nuevo.liga = actual.liga
    actual.liga = nuevo
    return P




def crear_rama(cabezas):
    """Crea una nueva rama cuyo último nodo apunta a un nodo ya existente."""
    if not todos_los_nodos(cabezas):
        print("Primero debe existir al menos un nodo.")
        return

    destino = buscar(cabezas, input("Dato del nodo al que apuntará la nueva rama: "))
    if destino is None:
        print("No se encontró ese nodo.")
        return

    cab = Nodo(input("Ingrese el dato del primer nodo de la rama: "))
    ultimo = cab
    res = int(input("¿Desea ingresar más nodos a la rama? Sí: 1, No: 0: "))
    while res == 1:
        q = Nodo(input("Ingrese el dato del nodo: "))
        ultimo.liga = q
        ultimo = q
        res = int(input("¿Desea ingresar más nodos a la rama? Sí: 1, No: 0: "))

    ultimo.liga = destino
    cabezas.append(cab)
    print(f"'{ultimo.info}' ahora apunta a '{destino.info}'.")


def enlazar(cabezas):
    """Hace que un nodo existente apunte a otro nodo existente."""
    origen = buscar(cabezas, input("Dato del nodo que va a apuntar (origen): "))
    destino = buscar(cabezas, input("Dato del nodo al que apuntará (destino): "))

    if origen is None or destino is None:
        print("No se encontró alguno de los nodos.")
        return
    if origen is destino or alcanza(destino, origen):
        print("No se permite: se formaría un ciclo.")
        return

    anterior = origen.liga
    origen.liga = destino
    print(f"'{origen.info}' ahora apunta a '{destino.info}'.")

    if anterior is not None and anterior not in todos_los_nodos(cabezas):
        print(f"Aviso: el nodo '{anterior.info}' y lo que le seguía quedaron desconectados.")




def eliminar(cabezas, dato):
    """Elimina el primer nodo con INFO = dato. Todos los nodos que apuntaban
    a él pasan a apuntar a su siguiente."""
    objetivo = buscar(cabezas, dato)
    if objetivo is None:
        print(f"El dato '{dato}' no se encontró en la lista.")
        return

    for nodo in todos_los_nodos(cabezas):
        if nodo.liga is objetivo:
            nodo.liga = objetivo.liga

    
    for i, cab in enumerate(cabezas):
        if cab is objetivo:
            cabezas[i] = objetivo.liga

   
    cabezas[:] = [c for i, c in enumerate(cabezas) if i == 0 or c is not None]
    print(f"Se eliminó el nodo '{dato}'.")



def menu(cabezas):
    while True:
        print("\n===== MENÚ =====")
        print("1. Insertar al principio")
        print("2. Insertar en medio (por posición)")
        print("3. Insertar al final")
        print("4. Eliminar un nodo")
        print("5. Mostrar lista")
        print("6. Crear rama que apunte a un nodo existente")
        print("7. Hacer que un nodo apunte a otro nodo")
        print("0. Salir")
        opcion = input("Elija una opción: ")

        if opcion in ("1", "2", "3"):
            P = cabezas[0]
            if opcion == "1":
                P = insertar_inicio(P, input("Dato a insertar: "))
            elif opcion == "2":
                dato = input("Dato a insertar: ")
                pos = int(input("Posición donde se insertará (1 = primer lugar): "))
                P = insertar_medio(P, dato, pos)
            else:
                P = insertar_final(P, input("Dato a insertar: "))
            cabezas[0] = P
        elif opcion == "4":
            eliminar(cabezas, input("Dato a eliminar: "))
        elif opcion == "5":
            pass
        elif opcion == "6":
            crear_rama(cabezas)
        elif opcion == "7":
            enlazar(cabezas)
        elif opcion == "0":
            print("Fin del programa.")
            break
        else:
            print("Opción no válida.")
            continue

        recorrer(cabezas)


if __name__ == "__main__":
    cabezas = [None]    
    print("Lista vacía. Use el menú para insertar nodos.")
    menu(cabezas)