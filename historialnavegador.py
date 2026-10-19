"""
Ejercicio 2: Historial de sitios visitados en un navegador web usando la clase Pila.

Se usan DOS pilas:
  - pila_atras:     sitios anteriores (para el botón "Atrás").
  - pila_adelante:  sitios a los que se puede regresar (botón "Adelante").
Además se guarda el sitio actual y una lista con el historial completo.
"""


class Pila:
    """Implementación de una pila (LIFO) usando una lista de Python."""

    def __init__(self):
        self.__items = []

    def apilar(self, elemento):
        self.__items.append(elemento)

    def desapilar(self):
        if self.esta_vacia():
            raise IndexError("La pila está vacía")
        return self.__items.pop()

    def cima(self):
        if self.esta_vacia():
            raise IndexError("La pila está vacía")
        return self.__items[-1]

    def esta_vacia(self):
        return len(self.__items) == 0

    def tamanio(self):
        return len(self.__items)

    def vaciar(self):
        self.__items.clear()

    def elementos(self):
        """Devuelve una copia de los elementos (de la base a la cima)."""
        return list(self.__items)


class Navegador:
    """Simula el historial de navegación de un navegador web."""

    def __init__(self):
        self.pila_atras = Pila()
        self.pila_adelante = Pila()
        self.actual = None
        self.historial = []  # registro cronológico de todos los sitios visitados

    def visitar(self, sitio):
        """Visita un nuevo sitio. El sitio actual pasa a la pila 'atrás'."""
        if self.actual is not None:
            self.pila_atras.apilar(self.actual)
        self.actual = sitio
        self.historial.append(sitio)
        # Al visitar un sitio nuevo, el historial "adelante" se descarta
        self.pila_adelante.vaciar()
        print(f"Visitando: {self.actual}")

    def atras(self):
        """Regresa al sitio anterior."""
        if self.pila_atras.esta_vacia():
            print("No hay sitios anteriores.")
            return
        self.pila_adelante.apilar(self.actual)
        self.actual = self.pila_atras.desapilar()
        print(f"Regresaste a: {self.actual}")

    def adelante(self):
        """Avanza al sitio del que se regresó."""
        if self.pila_adelante.esta_vacia():
            print("No hay sitios hacia adelante.")
            return
        self.pila_atras.apilar(self.actual)
        self.actual = self.pila_adelante.desapilar()
        print(f"Avanzaste a: {self.actual}")

    def mostrar_actual(self):
        if self.actual is None:
            print("No has visitado ningún sitio.")
        else:
            print(f"Sitio actual: {self.actual}")

    def mostrar_historial(self):
        if not self.historial:
            print("El historial está vacío.")
            return
        print("\n--- Historial (más reciente primero) ---")
        for i, sitio in enumerate(reversed(self.historial), start=1):
            print(f"{i}. {sitio}")

    def mostrar_pilas(self):
        print(f"Pila atrás:     {self.pila_atras.elementos()}")
        print(f"Sitio actual:   {self.actual}")
        print(f"Pila adelante:  {self.pila_adelante.elementos()}")

    def borrar_historial(self):
        self.pila_atras.vaciar()
        self.pila_adelante.vaciar()
        self.historial.clear()
        self.actual = None
        print("Historial borrado.")


def menu():
    navegador = Navegador()
    print("=" * 45)
    print("   HISTORIAL DE NAVEGADOR WEB (con Pilas)")
    print("=" * 45)

    while True:
        print("\n1. Visitar sitio")
        print("2. Atrás")
        print("3. Adelante")
        print("4. Ver sitio actual")
        print("5. Ver historial completo")
        print("6. Ver estado de las pilas")
        print("7. Borrar historial")
        print("8. Salir")
        opcion = input("Elige una opción: ").strip()

        if opcion == "1":
            sitio = input("Escribe la dirección (ej: www.google.com): ").strip()
            if sitio:
                navegador.visitar(sitio)
            else:
                print("La dirección no puede estar vacía.")
        elif opcion == "2":
            navegador.atras()
        elif opcion == "3":
            navegador.adelante()
        elif opcion == "4":
            navegador.mostrar_actual()
        elif opcion == "5":
            navegador.mostrar_historial()
        elif opcion == "6":
            navegador.mostrar_pilas()
        elif opcion == "7":
            navegador.borrar_historial()
        elif opcion == "8":
            print("¡Hasta luego!")
            break
        else:
            print("Opción no válida.")


if __name__ == "__main__":
    menu()