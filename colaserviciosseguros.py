"""Ejercicio 2: sistema de colas de servicios para una compañía de seguros.

Comandos (por consola):
    C <n>  -> Llega un cliente al servicio n; se le entrega su número.
    A <n>  -> Se atiende al siguiente cliente del servicio n.
    V      -> Ver el estado de todas las colas (opcional).
    S      -> Salir.
"""


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



SERVICIOS = {
    1: "Siniestros",
    2: "Contratación de pólizas",
    3: "Pagos y facturación",
    4: "Reclamos y atención general",
}


class SistemaAtencion:
    """Maneja una cola y un contador de tickets por cada servicio."""

    def __init__(self, servicios):
        self.servicios = servicios
        self.colas = {numero: Cola() for numero in servicios}
        self.ultimo_numero = {numero: 0 for numero in servicios}

    def llegada_cliente(self, servicio):
        """Entrega el siguiente número del servicio y lo encola."""
        self.ultimo_numero[servicio] += 1
        numero = self.ultimo_numero[servicio]
        self.colas[servicio].encolar(numero)
        return numero

    def atender_cliente(self, servicio):
        """Llama al siguiente cliente del servicio.

        Devuelve el número llamado o None si no hay clientes esperando.
        """
        cola = self.colas[servicio]
        if cola.esta_vacia():
            return None
        return cola.desencolar()

    def estado(self):
        """Devuelve un texto con el estado de todas las colas."""
        lineas = []
        for numero, nombre in self.servicios.items():
            lineas.append(
                f"  Servicio {numero} ({nombre}): "
                f"{self.colas[numero].tamanio()} en espera {self.colas[numero]}"
            )
        return "\n".join(lineas)


def mostrar_menu(servicios):
    print("=" * 56)
    print("   COMPAÑÍA DE SEGUROS - SISTEMA DE TURNOS")
    print("=" * 56)
    print("Servicios disponibles:")
    for numero, nombre in servicios.items():
        print(f"  {numero}. {nombre}")
    print()
    print("Comandos:")
    print("  C <n>  Llegada de un cliente al servicio n (ej: C 1)")
    print("  A <n>  Atender un cliente del servicio n   (ej: A 1)")
    print("  V      Ver estado de las colas")
    print("  S      Salir")
    print("-" * 56)


def procesar_comando(sistema, texto):
    """Procesa una línea ingresada. Devuelve False si se debe salir."""
    partes = texto.strip().upper().split()

    if not partes:
        return True

    comando = partes[0]

    if comando == "S" and len(partes) == 1:
        print("Cerrando el sistema. ¡Hasta luego!")
        return False

    if comando == "V" and len(partes) == 1:
        print(sistema.estado())
        return True

    
    if len(partes) == 1 and len(comando) > 1 and comando[0] in ("C", "A"):
        partes = [comando[0], comando[1:]]
        comando = partes[0]

    if comando not in ("C", "A") or len(partes) != 2:
        print("Comando inválido. Use: C <servicio>, A <servicio>, V o S.")
        return True

    if not partes[1].isdigit() or int(partes[1]) not in sistema.servicios:
        opciones = ", ".join(str(n) for n in sistema.servicios)
        print(f"Servicio inválido. Los servicios disponibles son: {opciones}.")
        return True

    servicio = int(partes[1])
    nombre = sistema.servicios[servicio]

    if comando == "C":
        numero = sistema.llegada_cliente(servicio)
        print(f"Cliente registrado en '{nombre}'. "
              f"Su número de atención es: {servicio}-{numero:03d}")
    else:
        numero = sistema.atender_cliente(servicio)
        if numero is None:
            print(f"No hay clientes en espera en '{nombre}'.")
        else:
            print(f"Llamando al número {servicio}-{numero:03d} "
                  f"({nombre})")

    return True


def main():
    sistema = SistemaAtencion(SERVICIOS)
    mostrar_menu(SERVICIOS)

    continuar = True
    while continuar:
        try:
            texto = input("> ")
        except (EOFError, KeyboardInterrupt):
            print("\nCerrando el sistema.")
            break
        continuar = procesar_comando(sistema, texto)


if __name__ == "__main__":
    main()