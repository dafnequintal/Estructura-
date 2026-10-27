"""MyLinkedList: listas enlazadas con ramas y nodos compartidos (UN SOLO ARCHIVO).

Cómo usarla
-----------
* Como biblioteca (desde otro programa en la MISMA carpeta):

      from MyLinkedList import ListaEnlazada
      lista = ListaEnlazada()
      lista.insertar_final("A")

  Importarla NO abre el menú ni pide datos.

* Menú interactivo:     python MyLinkedList.py
* Pruebas automáticas:  python MyLinkedList.py --pruebas
* Demostración:         python MyLinkedList.py --demo

Reglas de comportamiento
------------------------
1. NO se permiten ciclos. ``enlazar`` los rechaza con ``CicloError``.
2. Identidad = objeto (``is``). El dato (``info``) sólo sirve para buscar.
3. Con datos duplicados, "el primero" es el primero del recorrido: principal
   de inicio a fin, luego cada rama en orden de registro, sin repetir nodos.
4. Posición al insertar: 1 = primer lugar. ``posicion <= 1`` o lista
   principal vacía -> al inicio; ``posicion > longitud`` -> al final.
5. Eliminar un nodo: todo nodo que apuntaba a él pasa a apuntar a su
   siguiente; toda cabeza que era ese nodo pasa a ser su siguiente. Una
   rama que quede vacía, repetida o que pase a empezar en un nodo ya
   alcanzable desde otra cabeza se descarta (no se pierde ningún nodo);
   la principal se conserva aunque quede vacía. El nodo eliminado queda
   con ``liga = None``.
6. Enlazar reemplaza la liga anterior del origen. Los nodos que por eso
   quedan inalcanzables NO se borran: por omisión el primero de ellos se
   registra como una rama nueva (``conservar_desconectados=True``).
"""

import builtins
import importlib.util
import sys
import unittest
from typing import Any, Dict, Iterable, List, Optional, Tuple
from unittest import mock





class ErrorListaEnlazada(Exception):
    """Clase base de todos los errores de la biblioteca."""


class NodoNoEncontradoError(ErrorListaEnlazada, ValueError):
    """Se usó un nodo que no pertenece a la estructura registrada."""


class CicloError(ErrorListaEnlazada, ValueError):
    """La operación formaría (o encontró) un ciclo, y los ciclos no se permiten."""




from typing import Any, Optional


class Nodo:
    """Un nodo con un dato (``info``) y un apuntador al siguiente (``liga``).

    La identidad de un nodo es el OBJETO, no su dato: dos nodos con el mismo
    ``info`` son nodos distintos. Por eso no se define ``__eq__``; para
    comparar nodos se usa ``is``.

    Atributos:
        info: dato almacenado (puede ser de cualquier tipo).
        liga: siguiente ``Nodo`` o ``None`` (equivale a NIL).
    """

    __slots__ = ("info", "liga")

    def __init__(self, info: Any = None, liga: Optional["Nodo"] = None) -> None:
        self.info = info
        self.liga = liga

    @property
    def dato(self) -> Any:
        """Consulta el dato almacenado (sinónimo de solo lectura de ``info``)."""
        return self.info

    @property
    def siguiente(self) -> Optional["Nodo"]:
        """Consulta el siguiente nodo (sinónimo de solo lectura de ``liga``)."""
        return self.liga

    def __repr__(self) -> str:
        return f"Nodo(info={self.info!r})"




from typing import Any, Dict, Iterable, List, Optional



def todos_los_nodos(cabezas: Iterable[Optional[Nodo]]) -> List[Nodo]:
    """Devuelve los nodos alcanzables desde las cabezas, sin repetir objetos.

    Orden determinista: primero la cabeza 0 (principal) hasta su final, luego
    la cabeza 1, etc.; un nodo ya visto no se vuelve a agregar.
    """
    vistos = set()
    nodos: List[Nodo] = []
    for cabeza in cabezas:
        actual = cabeza
        while actual is not None and id(actual) not in vistos:
            vistos.add(id(actual))
            nodos.append(actual)
            actual = actual.liga
    return nodos


def contiene_nodo(cabezas: Iterable[Optional[Nodo]], nodo: Any) -> bool:
    """True si ese OBJETO nodo es alcanzable desde alguna cabeza (compara con ``is``)."""
    return any(n is nodo for n in todos_los_nodos(cabezas))


def buscar_nodo(cabezas: Iterable[Optional[Nodo]], dato: Any) -> Optional[Nodo]:
    """Devuelve el PRIMER nodo cuyo ``info == dato``, o ``None``.

    Criterio de "primero": el orden de ``todos_los_nodos`` (principal de
    inicio a fin, luego cada rama en el orden en que se registró).
    """
    for nodo in todos_los_nodos(cabezas):
        if nodo.info == dato:
            return nodo
    return None


def es_alcanzable(desde: Optional[Nodo], objetivo: Optional[Nodo]) -> bool:
    """True si siguiendo las ``liga`` desde ``desde`` se llega a ``objetivo``.

    Un nodo es alcanzable desde sí mismo. No se queda en bucle si hay ciclos.
    """
    vistos = set()
    actual = desde
    while actual is not None and id(actual) not in vistos:
        if actual is objetivo:
            return True
        vistos.add(id(actual))
        actual = actual.liga
    return False


def contar_apuntadores(cabezas: Iterable[Optional[Nodo]]) -> Dict[int, int]:
    """Cuenta cuántos nodos alcanzables apuntan (con ``liga``) a cada nodo.

    Devuelve ``{id(nodo_apuntado): cantidad}``.
    """
    conteo: Dict[int, int] = {}
    for nodo in todos_los_nodos(cabezas):
        if nodo.liga is not None:
            conteo[id(nodo.liga)] = conteo.get(id(nodo.liga), 0) + 1
    return conteo


def nodos_compartidos(cabezas: Iterable[Optional[Nodo]]) -> List[Nodo]:
    """Nodos a los que apuntan dos o más nodos (en orden de recorrido)."""
    cabezas = list(cabezas)
    conteo = contar_apuntadores(cabezas)
    return [n for n in todos_los_nodos(cabezas) if conteo.get(id(n), 0) >= 2]


def formatear(cabezas: Iterable[Optional[Nodo]], marca: str = "*") -> str:
    """Devuelve el texto de la lista principal y las ramas (no imprime).

    Ejemplo::

        Principal: A -> B* -> NIL
        Rama 1: X -> B* -> NIL
        (* = nodo al que apuntan dos o más nodos)

    Si una cadena entra en un ciclo se corta con ``(ciclo hacia <dato>)``.
    """
    cabezas = list(cabezas)
    if not any(c is not None for c in cabezas):
        return "La lista está vacía (NIL)"

    conteo = contar_apuntadores(cabezas)
    lineas = []
    hay_compartidos = False
    for i, cabeza in enumerate(cabezas):
        if cabeza is None and i != 0:
            continue
        etiqueta = "Principal" if i == 0 else f"Rama {i}"
        partes = []
        vistos = set()
        actual = cabeza
        hubo_ciclo = False
        while actual is not None:
            if id(actual) in vistos:
                partes.append(f"(ciclo hacia {actual.info})")
                hubo_ciclo = True
                break
            vistos.add(id(actual))
            m = marca if conteo.get(id(actual), 0) >= 2 else ""
            if m:
                hay_compartidos = True
            partes.append(f"{actual.info}{m}")
            actual = actual.liga
        if not hubo_ciclo:
            partes.append("NIL")
        lineas.append(f"{etiqueta}: " + " -> ".join(partes))
    if hay_compartidos:
        lineas.append(f"({marca} = nodo al que apuntan dos o más nodos)")
    return "\n".join(lineas)


# ======================================================================
# LISTA ENLAZADA (API PRINCIPAL)
# ======================================================================

from typing import Any, Iterable, List, Optional, Tuple



class ListaEnlazada:
    """Lista enlazada con ramas y nodos compartidos."""

    def __init__(self) -> None:
        """Crea una estructura vacía (lista principal vacía, sin ramas)."""
        self._cabezas: List[Optional[Nodo]] = [None]

    @classmethod
    def desde_iterable(cls, datos: Iterable[Any]) -> "ListaEnlazada":
        """Crea una lista principal con los datos dados, en ese orden."""
        lista = cls()
        ultimo = None
        for dato in datos:
            nuevo = Nodo(dato)
            if ultimo is None:
                lista._cabezas[0] = nuevo
            else:
                ultimo.liga = nuevo
            ultimo = nuevo
        return lista

    # ------------------------------------------------------------------
    # Administración y consulta de nodos
    # ------------------------------------------------------------------
    @staticmethod
    def crear_nodo(info: Any) -> Nodo:
        """Crea un nodo suelto (no queda registrado en la estructura)."""
        return Nodo(info)

    @property
    def cabeza(self) -> Optional[Nodo]:
        """Cabeza de la lista principal (``None`` si está vacía)."""
        return self._cabezas[0]

    @property
    def ramas(self) -> Tuple[Nodo, ...]:
        """Cabezas de las ramas registradas, en orden de registro."""
        return tuple(self._cabezas[1:])  # type: ignore[arg-type]

    @property
    def cabezas(self) -> Tuple[Optional[Nodo], ...]:
        """Todas las cabezas: la principal primero y luego las ramas."""
        return tuple(self._cabezas)

    def esta_vacia(self) -> bool:
        """True si no hay ningún nodo en la estructura (ni principal ni ramas)."""
        return all(c is None for c in self._cabezas)

    def longitud(self) -> int:
        """Cantidad de nodos de la lista PRINCIPAL (sin contar ramas)."""
        return len(todos_los_nodos([self._cabezas[0]]))

    def nodos(self) -> List[Nodo]:
        """Todos los nodos alcanzables (principal y ramas) sin repetir objetos."""
        return todos_los_nodos(self._cabezas)

    def nodos_principal(self) -> List[Nodo]:
        """Nodos de la lista principal, de inicio a fin."""
        return todos_los_nodos([self._cabezas[0]])

    def datos(self) -> List[Any]:
        """Datos (``info``) de la lista principal, de inicio a fin."""
        return [n.info for n in self.nodos_principal()]

    def contiene(self, nodo: Any) -> bool:
        """True si ese OBJETO nodo está en la estructura (compara con ``is``)."""
        return contiene_nodo(self._cabezas, nodo)

    # ------------------------------------------------------------------
    # Inserción (sólo lista principal; las ramas no se tocan)
    # ------------------------------------------------------------------
    def insertar_inicio(self, info: Any) -> Nodo:
        """Inserta al principio de la lista principal y devuelve el nodo nuevo."""
        nuevo = Nodo(info, self._cabezas[0])
        self._cabezas[0] = nuevo
        return nuevo

    def insertar_final(self, info: Any) -> Nodo:
        """Inserta al final de la lista principal y devuelve el nodo nuevo.

        Lanza ``CicloError`` si la principal tuviera un ciclo (no debería).
        """
        nuevo = Nodo(info)
        if self._cabezas[0] is None:
            self._cabezas[0] = nuevo
            return nuevo
        actual = self._cabezas[0]
        vistos = {id(actual)}
        while actual.liga is not None:
            actual = actual.liga
            if id(actual) in vistos:
                raise CicloError("La lista principal contiene un ciclo.")
            vistos.add(id(actual))
        actual.liga = nuevo
        return nuevo

    def insertar_en_posicion(self, info: Any, posicion: int) -> Nodo:
        """Inserta en la ``posicion`` indicada (1 = primer lugar).

        * ``posicion <= 1`` o lista principal vacía -> al inicio.
        * ``posicion`` mayor que la longitud -> al final.
        """
        if not isinstance(posicion, int) or isinstance(posicion, bool):
            raise TypeError("La posición debe ser un número entero.")
        if self._cabezas[0] is None or posicion <= 1:
            return self.insertar_inicio(info)
        actual = self._cabezas[0]
        for _ in range(posicion - 2):
            if actual.liga is None:
                break
            actual = actual.liga
        nuevo = Nodo(info, actual.liga)
        actual.liga = nuevo
        return nuevo

    # ------------------------------------------------------------------
    # Búsqueda
    # ------------------------------------------------------------------
    def buscar(self, dato: Any) -> Optional[Nodo]:
        """Primer nodo con ``info == dato`` (criterio en la doc del módulo) o ``None``."""
        return buscar_nodo(self._cabezas, dato)

    def buscar_todos(self, dato: Any) -> List[Nodo]:
        """Todos los nodos con ``info == dato``, en orden de recorrido."""
        return [n for n in self.nodos() if n.info == dato]

    def es_alcanzable(self, desde: Optional[Nodo], objetivo: Optional[Nodo]) -> bool:
        """True si desde ``desde`` se llega a ``objetivo`` (un nodo se alcanza a sí mismo)."""
        return es_alcanzable(desde, objetivo)

    # ------------------------------------------------------------------
    # Eliminación
    # ------------------------------------------------------------------
    def eliminar(self, dato: Any) -> Optional[Nodo]:
        """Elimina el primer nodo con ese dato. Devuelve el nodo o ``None`` si no existe."""
        objetivo = self.buscar(dato)
        if objetivo is None:
            return None
        return self.eliminar_nodo(objetivo)

    def eliminar_nodo(self, nodo: Nodo) -> Nodo:
        """Elimina ESE objeto nodo de la estructura (ver regla 5 del módulo).

        Lanza ``NodoNoEncontradoError`` si el nodo no está en la estructura.
        Devuelve el nodo eliminado, que queda con ``liga = None``.
        """
        self._exigir_en_estructura(nodo, "nodo")
        siguiente = nodo.liga
        if siguiente is nodo:
            siguiente = None
        for otro in todos_los_nodos(self._cabezas):
            if otro is not nodo and otro.liga is nodo:
                otro.liga = siguiente
        for i, cabeza in enumerate(self._cabezas):
            if cabeza is nodo:
                self._cabezas[i] = siguiente
                # Una rama que pasa a empezar en un nodo ya alcanzable desde
                # otra cabeza sería redundante: se descarta (sin perder nodos).
                if i >= 1 and siguiente is not None and any(
                        es_alcanzable(otra, siguiente)
                        for j, otra in enumerate(self._cabezas) if j != i):
                    self._cabezas[i] = None
        self._depurar_cabezas()
        nodo.liga = None
        return nodo

    # ------------------------------------------------------------------
    # Ramas y enlaces
    # ------------------------------------------------------------------
    def crear_rama(self, destino: Nodo, *datos: Any) -> Nodo:
        """Crea una rama nueva cuyo último nodo apunta a ``destino``.

        ``destino`` debe ser un nodo existente (objeto) de la estructura.
        Se necesita al menos un dato. Devuelve la cabeza de la rama.
        No se crean copias de ``destino``: queda compartido.
        """
        if not datos:
            raise ValueError("Una rama necesita al menos un dato.")
        self._exigir_en_estructura(destino, "destino")
        cabeza = ultimo = Nodo(datos[0])
        for dato in datos[1:]:
            ultimo.liga = Nodo(dato)
            ultimo = ultimo.liga
        ultimo.liga = destino
        self._cabezas.append(cabeza)
        return cabeza

    def enlazar(self, origen: Nodo, destino: Nodo,
                conservar_desconectados: bool = True) -> List[Nodo]:
        """Hace que ``origen.liga`` sea ``destino`` (ambos ya existentes).

        * Lanza ``CicloError`` si se formaría un ciclo (incluye origen is destino).
        * Lanza ``NodoNoEncontradoError`` si algún nodo no está en la estructura.
        * Devuelve la lista de nodos que quedaron inalcanzables (vacía si ninguno).
          Con ``conservar_desconectados=True`` el primero de ellos se registra
          como rama nueva para que ninguno se pierda; con ``False`` quedan
          fuera de la estructura (nada se borra, pero ya no se recorren).
        """
        self._exigir_en_estructura(origen, "origen")
        self._exigir_en_estructura(destino, "destino")
        if origen is destino or es_alcanzable(destino, origen):
            raise CicloError("No se permite: se formaría un ciclo.")
        anterior = origen.liga
        if anterior is destino:
            return []
        antes = todos_los_nodos(self._cabezas)
        origen.liga = destino
        despues = {id(n) for n in todos_los_nodos(self._cabezas)}
        desconectados = [n for n in antes if id(n) not in despues]
        if desconectados and conservar_desconectados:
            self._cabezas.append(anterior)
        return desconectados

    # ------------------------------------------------------------------
    # Nodos compartidos y visualización
    # ------------------------------------------------------------------
    def nodos_compartidos(self) -> List[Nodo]:
        """Nodos a los que apuntan dos o más nodos."""
        return nodos_compartidos(self._cabezas)

    def predecesores(self, nodo: Nodo) -> List[Nodo]:
        """Nodos de la estructura cuya ``liga`` es ese nodo."""
        return [n for n in self.nodos() if n.liga is nodo]

    def a_texto(self) -> str:
        """Representación textual de la principal y las ramas (no imprime)."""
        return formatear(self._cabezas)

    def mostrar(self) -> None:
        """Imprime ``a_texto()``. Es opcional: ninguna otra operación imprime."""
        print(self.a_texto())

    # ------------------------------------------------------------------
    # Nombres estándar (atajos de los métodos anteriores)
    # ------------------------------------------------------------------
    def append(self, valor: Any) -> Nodo:
        """Agrega al final de la lista principal (igual que ``insertar_final``)."""
        return self.insertar_final(valor)

    def prepend(self, valor: Any) -> Nodo:
        """Agrega al inicio de la lista principal (igual que ``insertar_inicio``)."""
        return self.insertar_inicio(valor)

    def find(self, valor: Any) -> Optional[Nodo]:
        """Primer nodo con ese dato o ``None`` (igual que ``buscar``)."""
        return self.buscar(valor)

    def delete(self, valor: Any) -> Optional[Nodo]:
        """Elimina el primer nodo con ese dato (igual que ``eliminar``)."""
        return self.eliminar(valor)

    def __len__(self) -> int:
        """``len(lista)`` = cantidad de nodos de la lista PRINCIPAL.

        Ojo: una lista principal vacía se evalúa como ``False`` en un ``if``.
        """
        return self.longitud()

    def __iter__(self):
        """Permite ``for dato in lista`` (recorre los datos de la principal)."""
        return iter(self.datos())

    def __contains__(self, valor: Any) -> bool:
        """``valor in lista``: True si algún nodo de la estructura tiene ese dato."""
        return self.buscar(valor) is not None

    def __str__(self) -> str:
        return self.a_texto()

    def __repr__(self) -> str:
        return f"ListaEnlazada(principal={self.datos()!r}, ramas={len(self._cabezas) - 1})"

    # ------------------------------------------------------------------
    # Auxiliares internos
    # ------------------------------------------------------------------
    def _exigir_en_estructura(self, nodo: Any, nombre: str) -> None:
        if not isinstance(nodo, Nodo):
            raise TypeError(f"'{nombre}' debe ser un Nodo.")
        if not contiene_nodo(self._cabezas, nodo):
            raise NodoNoEncontradoError(f"El {nombre} no pertenece a la estructura.")

    def _depurar_cabezas(self) -> None:
        """Descarta ramas vacías o repetidas; conserva siempre la principal."""
        principal = self._cabezas[0]
        nuevas: List[Optional[Nodo]] = [principal]
        vistos = {id(principal)} if principal is not None else set()
        for cabeza in self._cabezas[1:]:
            if cabeza is None or id(cabeza) in vistos:
                continue
            vistos.add(id(cabeza))
            nuevas.append(cabeza)
        self._cabezas[:] = nuevas


# Nombres alternativos en inglés
LinkedList = ListaEnlazada
Node = Nodo


# ======================================================================
# MENÚ INTERACTIVO (ejemplo, no forma parte del núcleo)
# ======================================================================



def pedir_entero(mensaje):
    while True:
        try:
            return int(input(mensaje))
        except ValueError:
            print("Escriba un número entero.")


def crear_rama(lista):
    if lista.esta_vacia():
        print("Primero debe existir al menos un nodo.")
        return
    destino = lista.buscar(input("Dato del nodo al que apuntará la nueva rama: "))
    if destino is None:
        print("No se encontró ese nodo.")
        return
    datos = [input("Ingrese el dato del primer nodo de la rama: ")]
    while pedir_entero("¿Desea ingresar más nodos a la rama? Sí: 1, No: 0: ") == 1:
        datos.append(input("Ingrese el dato del nodo: "))
    lista.crear_rama(destino, *datos)
    print(f"'{datos[-1]}' ahora apunta a '{destino.info}'.")


def enlazar(lista):
    origen = lista.buscar(input("Dato del nodo que va a apuntar (origen): "))
    destino = lista.buscar(input("Dato del nodo al que apuntará (destino): "))
    if origen is None or destino is None:
        print("No se encontró alguno de los nodos.")
        return
    try:
        perdidos = lista.enlazar(origen, destino)
    except (CicloError, NodoNoEncontradoError) as error:
        print(error)
        return
    print(f"'{origen.info}' ahora apunta a '{destino.info}'.")
    if perdidos:
        print(f"Aviso: {len(perdidos)} nodo(s) quedaron desconectados de la lista "
              f"principal; se conservaron como una rama nueva.")


def menu(lista):
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

        if opcion == "1":
            lista.insertar_inicio(input("Dato a insertar: "))
        elif opcion == "2":
            dato = input("Dato a insertar: ")
            lista.insertar_en_posicion(
                dato, pedir_entero("Posición donde se insertará (1 = primer lugar): "))
        elif opcion == "3":
            lista.insertar_final(input("Dato a insertar: "))
        elif opcion == "4":
            dato = input("Dato a eliminar: ")
            if lista.eliminar(dato) is None:
                print(f"El dato '{dato}' no se encontró en la lista.")
            else:
                print(f"Se eliminó el nodo '{dato}'.")
        elif opcion == "5":
            pass
        elif opcion == "6":
            crear_rama(lista)
        elif opcion == "7":
            enlazar(lista)
        elif opcion == "0":
            print("Fin del programa.")
            break
        else:
            print("Opción no válida.")
            continue
        lista.mostrar()


# ======================================================================
# PRUEBAS AUTOMÁTICAS (python MyLinkedList.py --pruebas)
# ======================================================================




def lista_abcd():
    """Principal A -> B -> C -> D."""
    return ListaEnlazada.desde_iterable(["A", "B", "C", "D"])


class TestCreacionEInsercion(unittest.TestCase):
    def test_01_lista_vacia(self):
        lista = ListaEnlazada()
        self.assertIsNone(lista.cabeza)
        self.assertTrue(lista.esta_vacia())
        self.assertEqual(lista.longitud(), 0)
        self.assertEqual(lista.ramas, ())
        self.assertEqual(lista.a_texto(), "La lista está vacía (NIL)")

    def test_02_insertar_inicio(self):
        lista = lista_abcd()
        nuevo = lista.insertar_inicio("Z")
        self.assertIs(lista.cabeza, nuevo)
        self.assertEqual(lista.datos(), ["Z", "A", "B", "C", "D"])

    def test_02b_insertar_inicio_en_vacia(self):
        lista = ListaEnlazada()
        lista.insertar_inicio(1)
        self.assertEqual(lista.datos(), [1])

    def test_03_insertar_final(self):
        lista = lista_abcd()
        lista.insertar_final("Z")
        self.assertEqual(lista.datos(), ["A", "B", "C", "D", "Z"])

    def test_03b_insertar_final_en_vacia(self):
        lista = ListaEnlazada()
        lista.insertar_final(1)
        lista.insertar_final(2)
        self.assertEqual(lista.datos(), [1, 2])

    def test_04_insertar_posicion_intermedia(self):
        lista = lista_abcd()
        lista.insertar_en_posicion("Z", 3)
        self.assertEqual(lista.datos(), ["A", "B", "Z", "C", "D"])

    def test_04b_posicion_menor_o_igual_a_1_va_al_inicio(self):
        for pos in (1, 0, -5):
            lista = lista_abcd()
            lista.insertar_en_posicion("Z", pos)
            self.assertEqual(lista.datos()[0], "Z")

    def test_04c_posicion_en_lista_vacia(self):
        lista = ListaEnlazada()
        lista.insertar_en_posicion("Z", 7)
        self.assertEqual(lista.datos(), ["Z"])

    def test_05_posicion_mayor_que_tamano_va_al_final(self):
        lista = lista_abcd()
        lista.insertar_en_posicion("Z", 99)
        self.assertEqual(lista.datos(), ["A", "B", "C", "D", "Z"])

    def test_05b_posicion_justo_despues_del_final(self):
        lista = lista_abcd()
        lista.insertar_en_posicion("Z", 5)
        self.assertEqual(lista.datos(), ["A", "B", "C", "D", "Z"])

    def test_05c_posicion_no_entera(self):
        with self.assertRaises(TypeError):
            lista_abcd().insertar_en_posicion("Z", "2")

    def test_tipos_de_datos_variados(self):
        objeto = object()
        lista = ListaEnlazada.desde_iterable([1, "dos", 3.0, None, objeto, [1]])
        self.assertIs(lista.buscar(objeto).info, objeto)
        self.assertEqual(lista.longitud(), 6)

    def test_insertar_conserva_ramas(self):
        lista = lista_abcd()
        d = lista.buscar("D")
        rama = lista.crear_rama(d, "X")
        lista.insertar_inicio("Z")
        lista.insertar_final("W")
        lista.insertar_en_posicion("M", 3)
        self.assertEqual(lista.ramas, (rama,))
        self.assertIs(rama.liga, d)


class TestBusqueda(unittest.TestCase):
    def test_06_buscar_existente(self):
        lista = lista_abcd()
        nodo = lista.buscar("C")
        self.assertEqual(nodo.info, "C")
        self.assertEqual(nodo.dato, "C")
        self.assertEqual(nodo.siguiente.info, "D")

    def test_07_buscar_inexistente(self):
        self.assertIsNone(lista_abcd().buscar("Z"))
        self.assertIsNone(ListaEnlazada().buscar("A"))

    def test_17_duplicados_primero_del_recorrido(self):
        lista = ListaEnlazada.desde_iterable(["A", "X", "B", "X"])
        todos = lista.buscar_todos("X")
        self.assertEqual(len(todos), 2)
        self.assertIs(lista.buscar("X"), lista.cabeza.liga)
        # El primero es el de la principal aunque una rama tenga otro igual
        lista.crear_rama(lista.buscar("B"), "X")
        self.assertIs(lista.buscar("X"), lista.cabeza.liga)

    def test_17b_busca_en_ramas(self):
        lista = lista_abcd()
        lista.crear_rama(lista.buscar("D"), "X", "Y")
        self.assertEqual(lista.buscar("Y").info, "Y")

    def test_es_alcanzable(self):
        lista = lista_abcd()
        a, d = lista.buscar("A"), lista.buscar("D")
        self.assertTrue(lista.es_alcanzable(a, d))
        self.assertFalse(lista.es_alcanzable(d, a))
        self.assertTrue(lista.es_alcanzable(a, a))

    def test_identidad_no_dato(self):
        lista = ListaEnlazada.desde_iterable(["X", "X"])
        primero, segundo = lista.nodos_principal()
        self.assertIsNot(primero, segundo)
        self.assertFalse(lista.es_alcanzable(segundo, primero))


class TestEliminacion(unittest.TestCase):
    def test_08_eliminar_primero(self):
        lista = lista_abcd()
        lista.eliminar("A")
        self.assertEqual(lista.datos(), ["B", "C", "D"])

    def test_09_eliminar_intermedio(self):
        lista = lista_abcd()
        lista.eliminar("C")
        self.assertEqual(lista.datos(), ["A", "B", "D"])

    def test_10_eliminar_ultimo(self):
        lista = lista_abcd()
        lista.eliminar("D")
        self.assertEqual(lista.datos(), ["A", "B", "C"])
        self.assertIsNone(lista.buscar("C").liga)

    def test_11_eliminar_inexistente(self):
        lista = lista_abcd()
        self.assertIsNone(lista.eliminar("Z"))
        self.assertEqual(lista.datos(), ["A", "B", "C", "D"])
        self.assertIsNone(ListaEnlazada().eliminar("A"))

    def test_eliminar_unico_deja_principal_vacia(self):
        lista = ListaEnlazada.desde_iterable(["A"])
        lista.eliminar("A")
        self.assertTrue(lista.esta_vacia())
        self.assertEqual(len(lista.cabezas), 1)

    def test_eliminar_devuelve_nodo_desligado(self):
        lista = lista_abcd()
        nodo = lista.eliminar("B")
        self.assertEqual(nodo.info, "B")
        self.assertIsNone(nodo.liga)
        self.assertFalse(lista.contiene(nodo))

    def test_eliminar_duplicado_elimina_solo_el_primero(self):
        lista = ListaEnlazada.desde_iterable(["X", "A", "X"])
        lista.eliminar("X")
        self.assertEqual(lista.datos(), ["A", "X"])

    def test_eliminar_nodo_por_identidad(self):
        lista = ListaEnlazada.desde_iterable(["X", "A", "X"])
        ultimo = lista.nodos_principal()[2]
        lista.eliminar_nodo(ultimo)
        self.assertEqual(lista.datos(), ["X", "A"])

    def test_eliminar_nodo_ajeno(self):
        lista = lista_abcd()
        with self.assertRaises(NodoNoEncontradoError):
            lista.eliminar_nodo(Nodo("A"))   # mismo dato, otro objeto
        with self.assertRaises(TypeError):
            lista.eliminar_nodo("A")


class TestRamasYCompartidos(unittest.TestCase):
    def test_12_crear_rama(self):
        lista = lista_abcd()
        c = lista.buscar("C")
        cab = lista.crear_rama(c, "X", "Y")
        self.assertEqual(cab.info, "X")
        self.assertEqual(lista.ramas, (cab,))
        self.assertIs(cab.liga.liga, c)

    def test_12b_crear_rama_errores(self):
        lista = lista_abcd()
        with self.assertRaises(ValueError):
            lista.crear_rama(lista.cabeza)           # sin datos
        with self.assertRaises(NodoNoEncontradoError):
            lista.crear_rama(Nodo("C"), "X")         # destino ajeno
        with self.assertRaises(NodoNoEncontradoError):
            ListaEnlazada().crear_rama(Nodo("C"), "X")

    def test_13_compartir_nodo_entre_rutas(self):
        lista = lista_abcd()
        c = lista.buscar("C")
        lista.crear_rama(c, "X")
        lista.crear_rama(c, "Y", "Z")
        self.assertEqual(len(lista.predecesores(c)), 3)
        # Misma identidad, sin copias
        self.assertEqual(len([n for n in lista.nodos() if n.info == "C"]), 1)

    def test_14_nodos_compartidos(self):
        lista = lista_abcd()
        self.assertEqual(lista.nodos_compartidos(), [])
        c = lista.buscar("C")
        lista.crear_rama(c, "X")
        self.assertEqual(lista.nodos_compartidos(), [c])
        texto = lista.a_texto()
        self.assertIn("C*", texto)
        self.assertIn("Rama 1: X -> C* -> D -> NIL", texto)
        self.assertNotIn("A*", texto)

    def test_nodos_sin_repetir(self):
        lista = lista_abcd()
        lista.crear_rama(lista.buscar("C"), "X")
        nodos = lista.nodos()
        self.assertEqual(len(nodos), 5)
        self.assertEqual(len({id(n) for n in nodos}), 5)

    def test_enlazar_basico(self):
        lista = lista_abcd()
        b, d = lista.buscar("B"), lista.buscar("D")
        perdidos = lista.enlazar(b, d)
        self.assertIs(b.liga, d)
        self.assertEqual([n.info for n in perdidos], ["C"])
        # C se conserva como rama
        self.assertEqual([r.info for r in lista.ramas], ["C"])
        self.assertIsNotNone(lista.buscar("C"))

    def test_enlazar_sin_conservar(self):
        lista = lista_abcd()
        b, d = lista.buscar("B"), lista.buscar("D")
        perdidos = lista.enlazar(b, d, conservar_desconectados=False)
        self.assertEqual([n.info for n in perdidos], ["C"])
        self.assertEqual(lista.ramas, ())
        self.assertIsNone(lista.buscar("C"))

    def test_enlazar_sin_perdidos_si_hay_otra_ruta(self):
        lista = lista_abcd()
        c = lista.buscar("C")
        lista.crear_rama(c, "X")
        a = lista.buscar("A")
        # A -> C: B queda inalcanzable, pero C sigue por la rama
        perdidos = lista.enlazar(a, c)
        self.assertEqual([n.info for n in perdidos], ["B"])

    def test_enlazar_mismo_destino_no_hace_nada(self):
        lista = lista_abcd()
        self.assertEqual(lista.enlazar(lista.buscar("A"), lista.buscar("B")), [])
        self.assertEqual(lista.ramas, ())

    def test_enlazar_nodo_ajeno(self):
        lista = lista_abcd()
        with self.assertRaises(NodoNoEncontradoError):
            lista.enlazar(lista.cabeza, Nodo("Z"))


class TestCiclos(unittest.TestCase):
    def test_15_rechaza_ciclos(self):
        lista = lista_abcd()
        a, d = lista.buscar("A"), lista.buscar("D")
        with self.assertRaises(CicloError):
            lista.enlazar(d, a)
        with self.assertRaises(CicloError):
            lista.enlazar(a, a)
        self.assertEqual(lista.datos(), ["A", "B", "C", "D"])  # sin cambios

    def test_15b_ciclo_via_rama(self):
        lista = lista_abcd()
        d = lista.buscar("D")
        x = lista.crear_rama(d, "X")
        with self.assertRaises(CicloError):
            lista.enlazar(d, x)

    def test_16_recorrido_no_se_bloquea_con_ciclo(self):
        a, b, c = Nodo("A"), Nodo("B"), Nodo("C")
        a.liga, b.liga, c.liga = b, c, a          # ciclo forzado a mano
        self.assertEqual(len(todos_los_nodos([a])), 3)
        self.assertFalse(es_alcanzable(a, Nodo("Z")))
        self.assertTrue(es_alcanzable(a, c))
        lista = ListaEnlazada()
        lista._cabezas[0] = a
        self.assertIn("ciclo hacia A", lista.a_texto())
        self.assertEqual(lista.longitud(), 3)
        with self.assertRaises(CicloError):
            lista.insertar_final("Z")

    def test_ciclo_ajeno_a_la_cabeza(self):
        a, b, c = Nodo("A"), Nodo("B"), Nodo("C")
        a.liga, b.liga, c.liga = b, c, b
        self.assertEqual(len(todos_los_nodos([a])), 3)


class TestEliminacionCompartida(unittest.TestCase):
    def test_19_eliminar_compartido_actualiza_referencias(self):
        lista = lista_abcd()                      # A B C D
        c, d = lista.buscar("C"), lista.buscar("D")
        y = lista.crear_rama(c, "Y")              # Y -> C
        w = lista.crear_rama(c, "W")              # W -> C
        lista.eliminar("C")
        self.assertIs(lista.buscar("B").liga, d)
        self.assertIs(y.liga, d)
        self.assertIs(w.liga, d)
        self.assertEqual(lista.nodos_compartidos(), [d])
        self.assertIsNone(lista.buscar("C"))

    def test_19b_eliminar_cabeza_de_rama(self):
        lista = lista_abcd()
        c = lista.buscar("C")
        x = lista.crear_rama(c, "X", "Y")
        y = x.liga
        lista.eliminar("X")
        self.assertEqual(lista.ramas, (y,))

    def test_19c_eliminar_unica_rama_de_un_nodo(self):
        lista = lista_abcd()
        c = lista.buscar("C")
        lista.crear_rama(c, "X")
        lista.eliminar("X")
        self.assertEqual(lista.ramas, ())
        self.assertEqual(lista.datos(), ["A", "B", "C", "D"])

    def test_19e_rama_apuntando_a_cabeza_pasa_al_siguiente(self):
        lista = lista_abcd()
        a, b = lista.buscar("A"), lista.buscar("B")
        x = lista.crear_rama(a, "X")
        lista.eliminar("A")
        self.assertIs(x.liga, b)
        self.assertIs(lista.cabeza, b)

    def test_19f_eliminar_ultimo_compartido(self):
        lista = lista_abcd()
        d = lista.buscar("D")
        x = lista.crear_rama(d, "X")
        lista.eliminar("D")
        self.assertIsNone(x.liga)
        self.assertIsNone(lista.buscar("C").liga)

    def test_19g_rama_redundante_se_descarta(self):
        lista = lista_abcd()
        c = lista.buscar("C")
        lista.crear_rama(c, "X")
        lista._cabezas.append(c)                  # C también registrada como rama
        lista.eliminar("X")                       # la cabeza X pasaría a ser C
        self.assertEqual(lista.ramas, (c,))       # sin cabezas repetidas

    def test_20_no_modifica_otras_ramas(self):
        lista = lista_abcd()
        c = lista.buscar("C")
        r1 = lista.crear_rama(c, "X", "Y")
        r2 = lista.crear_rama(c, "P", "Q")
        antes_r2 = [n.info for n in todos_los_nodos([r2])]
        lista.eliminar("X")                       # sólo toca la rama 1
        lista.insertar_inicio("Z")
        self.assertEqual([n.info for n in todos_los_nodos([r2])], antes_r2)
        self.assertIn(r2, lista.ramas)
        self.assertEqual([n.info for n in todos_los_nodos([lista.ramas[0]])],
                         ["Y", "C", "D"])


class TestNombresEstandar(unittest.TestCase):
    def test_append_prepend_len_iter(self):
        lista = LinkedList()
        lista.append(2)
        lista.append(3)
        lista.prepend(1)
        self.assertEqual(len(lista), 3)
        self.assertEqual(list(lista), [1, 2, 3])
        self.assertEqual(str(lista), "Principal: 1 -> 2 -> 3 -> NIL")

    def test_find_delete_in(self):
        lista = LinkedList.desde_iterable(["a", "b", "c"])
        self.assertIn("b", lista)
        self.assertEqual(lista.find("b").info, "b")
        lista.delete("b")
        self.assertNotIn("b", lista)
        self.assertIsNone(lista.find("b"))
        self.assertIsNone(lista.delete("zzz"))
        self.assertEqual(len(lista), 2)

    def test_alias_son_las_mismas_clases(self):
        self.assertIs(LinkedList, ListaEnlazada)
        self.assertIs(Node, Nodo)


class TestImportacion(unittest.TestCase):
    def test_18_importar_sin_menu_ni_input(self):
        def prohibido(*args, **kwargs):
            raise AssertionError("La biblioteca no debe llamar a input()")

        especificacion = importlib.util.spec_from_file_location(
            "mylinkedlist_importada", __file__)
        paquete = importlib.util.module_from_spec(especificacion)
        with mock.patch.object(builtins, "input", prohibido), \
                mock.patch.object(builtins, "print", prohibido):
            especificacion.loader.exec_module(paquete)
            lista = paquete.ListaEnlazada.desde_iterable([1, 2, 3])
            lista.insertar_final(4)
            lista.crear_rama(lista.buscar(3), 9)
            lista.enlazar(lista.buscar(1), lista.buscar(3))
            lista.eliminar(2)
            lista.a_texto()
        # Si el menú se hubiera ejecutado al importar, input() habría fallado arriba.
        self.assertTrue(callable(paquete.menu))


# ======================================================================
# DEMOSTRACIÓN
# ======================================================================

def demo():
    """Ejemplo de uso sin menú."""
    lista = ListaEnlazada()
    lista.insertar_final("B")
    lista.insertar_final("D")
    lista.insertar_inicio("A")
    lista.insertar_en_posicion("C", 3)
    print("Principal:", lista.datos())
    nodo_d = lista.buscar("D")
    lista.crear_rama(nodo_d, "X", "Y")
    print("\nCon rama:\n" + lista.a_texto())
    perdidos = lista.enlazar(lista.buscar("B"), nodo_d)
    print("\nDespués de enlazar B -> D:\n" + lista.a_texto())
    print("Desconectados:", perdidos)
    try:
        lista.enlazar(nodo_d, lista.buscar("A"))
    except CicloError as error:
        print("\nRechazado:", error)
    print("Compartidos:", lista.nodos_compartidos())
    lista.eliminar("D")
    print("\nDespués de eliminar D:\n" + lista.a_texto())


# ======================================================================
# PROGRAMA PRINCIPAL (no se ejecuta al importar)
# ======================================================================

if __name__ == "__main__":
    if "--pruebas" in sys.argv:
        sys.argv.remove("--pruebas")
        unittest.main(verbosity=2)
    elif "--demo" in sys.argv:
        demo()
    else:
        print("Lista vacía. Use el menú para insertar nodos.")
        menu(ListaEnlazada())