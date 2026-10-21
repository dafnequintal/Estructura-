"""Ejercicio 1: suma elemento a elemento de dos colas de enteros."""


class Nodo:
    """Nodo de una lista enlazada simple."""

    def __init__(self, dato):
        self.dato = dato
        self.siguiente = None


class Cola:
    """Cola FIFO implementada con nodos enlazados.

    Operaciones O(1): encolar, desencolar, frente, esta_vacia, tamanio.
    """

    def __init__(self):
        self._frente = None
        self._final = None
        self._tamanio = 0

    def encolar(self, dato):
        """Agrega un elemento al final de la cola."""
        nuevo = Nodo(dato)
        if self.esta_vacia():
            self._frente = nuevo
        else:
            self._final.siguiente = nuevo
        self._final = nuevo
        self._tamanio += 1

    def desencolar(self):
        """Elimina y devuelve el elemento del frente de la cola."""
        if self.esta_vacia():
            raise IndexError("La cola está vacía")
        dato = self._frente.dato
        self._frente = self._frente.siguiente
        if self._frente is None:
            self._final = None
        self._tamanio -= 1
        return dato

    def frente(self):
        """Devuelve el elemento del frente sin eliminarlo."""
        if self.esta_vacia():
            raise IndexError("La cola está vacía")
        return self._frente.dato

    def esta_vacia(self):
        return self._tamanio == 0

    def tamanio(self):
        return self._tamanio

    def __len__(self):
        return self._tamanio

    def __str__(self):
        elementos = []
        actual = self._frente
        while actual is not None:
            elementos.append(str(actual.dato))
            actual = actual.siguiente
        return "[" + ", ".join(elementos) + "]"


def sumar_colas(cola_a, cola_b):
    """Recibe dos colas de enteros y devuelve una nueva cola con la suma
    de sus elementos uno a uno.

    - Las colas originales NO se modifican (se restauran al terminar).
    - Si las colas tienen distinto tamaño, el elemento faltante se
      considera 0, de modo que no se pierde ningún dato.
    """
    resultado = Cola()
    aux_a = Cola()
    aux_b = Cola()

    while not cola_a.esta_vacia() or not cola_b.esta_vacia():
        valor_a = 0
        valor_b = 0

        if not cola_a.esta_vacia():
            valor_a = cola_a.desencolar()
            aux_a.encolar(valor_a)
        if not cola_b.esta_vacia():
            valor_b = cola_b.desencolar()
            aux_b.encolar(valor_b)

        resultado.encolar(valor_a + valor_b)

    while not aux_a.esta_vacia():
        cola_a.encolar(aux_a.desencolar())
    while not aux_b.esta_vacia():
        cola_b.encolar(aux_b.desencolar())

    return resultado


def crear_cola(valores):
    """Crea una Cola a partir de una lista de enteros."""
    cola = Cola()
    for v in valores:
        cola.encolar(v)
    return cola


def mostrar_tabla(cola_a, cola_b, cola_resultado):
    """Muestra las tres colas en formato de tabla."""
    a = str(cola_a)[1:-1].split(", ") if not cola_a.esta_vacia() else []
    b = str(cola_b)[1:-1].split(", ") if not cola_b.esta_vacia() else []
    r = str(cola_resultado)[1:-1].split(", ") if not cola_resultado.esta_vacia() else []

    print(f"{'Cola A':>8} {'Cola B':>8} {'Resultado':>10}")
    for i in range(len(r)):
        va = a[i] if i < len(a) else "-"
        vb = b[i] if i < len(b) else "-"
        print(f"{va:>8} {vb:>8} {r[i]:>10}")


def main():
    cola_a = crear_cola([3, 4, 2, 8, 12])
    cola_b = crear_cola([6, 2, 9, 11, 3])

    resultado = sumar_colas(cola_a, cola_b)
    mostrar_tabla(cola_a, cola_b, resultado)


if __name__ == "__main__":
    main()