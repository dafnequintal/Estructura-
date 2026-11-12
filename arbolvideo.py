"""
Árbol Binario de Búsqueda (ABB)
Estructuras de Datos - Unidad VII. Árboles

Implementa la clase Nodo, la clase Arbol y los métodos vistos en clase:
inserción, búsqueda, recorridos, eliminación (predecesor / sucesor),
altura, conteo de hojas y nodos, árbol completo, árbol lleno y poda.
"""

from collections import deque


class Nodo:
    """Nodo del árbol: guarda un dato y los enlaces a sus dos hijos."""

    def __init__(self, dato):
        self.dato = dato
        self.izquierdo = None
        self.derecho = None


class Arbol:
    """Árbol binario de búsqueda: menores a la izquierda, mayores a la derecha."""

    def __init__(self):
        self.raiz = None

   
    def es_vacio(self):
        return self.raiz is None

    def regresa_raiz(self):
        return self.raiz

    def insertar(self, valor):
        """Inserta un valor. Si ya existe, no lo duplica."""
        self.raiz = self._insertar(valor, self.raiz)

    def _insertar(self, valor, nodo):
        if nodo is None:                     
            return Nodo(valor)
        if valor < nodo.dato:
            nodo.izquierdo = self._insertar(valor, nodo.izquierdo)
        elif valor > nodo.dato:
            nodo.derecho = self._insertar(valor, nodo.derecho)
        else:
            print(f"El valor {valor} ya existe en el árbol.")
        return nodo

    def buscar(self, x):
        return self._buscar(x, self.raiz)

    def _buscar(self, x, nodo):
        if nodo is None:                     
            return False
        if x < nodo.dato:
            return self._buscar(x, nodo.izquierdo)
        if x > nodo.dato:
            return self._buscar(x, nodo.derecho)
        return True                          
    
    
    def muestra_acostado(self):
        """Imprime el árbol horizontal (raíz a la izquierda) con ramas dibujadas."""
        if self.es_vacio():
            print("El árbol está vacío.")
            return
        self._acostado(self.raiz.derecho, "", True)
        print(self.raiz.dato)
        self._acostado(self.raiz.izquierdo, "", False)

    def _acostado(self, nodo, prefijo, es_superior):
        if nodo is None:
            return
        
        self._acostado(nodo.derecho, prefijo + ("    " if es_superior else "│   "), True)
        print(prefijo + ("┌── " if es_superior else "└── ") + str(nodo.dato))
        self._acostado(nodo.izquierdo, prefijo + ("│   " if es_superior else "    "), False)

    def graficar(self):
        """Dibuja el árbol en forma vertical, con la raíz arriba."""
        if self.es_vacio():
            print("El árbol está vacío.")
            return
        lineas, _, _ = self._graficar(self.raiz)
        print("\n".join(lineas))

    def _graficar(self, nodo):
        """Devuelve (líneas, ancho, posición_del_centro) del subárbol."""
        texto = str(nodo.dato)
        if nodo.izquierdo is None and nodo.derecho is None:
            return [texto], len(texto), len(texto) // 2

        izq = self._graficar(nodo.izquierdo) if nodo.izquierdo else None
        der = self._graficar(nodo.derecho) if nodo.derecho else None

        
        if der is None:
            l, w, c = izq
            primera = " " * (c + 1) + "_" * (w - c - 1) + texto
            segunda = " " * c + "/" + " " * (w - c - 1 + len(texto))
            return ([primera, segunda] + [x + " " * len(texto) for x in l],
                    w + len(texto), w + len(texto) // 2)
        if izq is None:
            l, w, c = der
            primera = texto + "_" * c + " " * (w - c)
            segunda = " " * (len(texto) + c) + "\\" + " " * (w - c - 1)
            return ([primera, segunda] + [" " * len(texto) + x for x in l],
                    w + len(texto), len(texto) // 2)

        # Dos hijos
        li, wi, ci = izq
        ld, wd, cd = der
        primera = (" " * (ci + 1) + "_" * (wi - ci - 1) + texto
                   + "_" * cd + " " * (wd - cd))
        segunda = (" " * ci + "/" + " " * (wi - ci - 1 + len(texto) + cd)
                   + "\\" + " " * (wd - cd - 1))
        if len(li) < len(ld):
            li += [" " * wi] * (len(ld) - len(li))
        else:
            ld += [" " * wd] * (len(li) - len(ld))
        cuerpo = [a + " " * len(texto) + b for a, b in zip(li, ld)]
        return ([primera, segunda] + cuerpo,
                wi + wd + len(texto), wi + len(texto) // 2)

    
    def calcular_posiciones(self, dx=64, dy=96, margen=60):
        """
        Calcula las coordenadas (x, y) de cada nodo.
        - x: posición del nodo en el recorrido InOrden (así nunca se encimen).
        - y: nivel del nodo (la raíz está arriba).
        Devuelve (posiciones, ancho, alto).
        """
        posiciones = {}
        contador = [0]

        def asignar(nodo, nivel):
            if nodo is None:
                return
            asignar(nodo.izquierdo, nivel + 1)
            posiciones[nodo] = (margen + contador[0] * dx, margen + 30 + (nivel * dy))
            contador[0] += 1
            asignar(nodo.derecho, nivel + 1)

        asignar(self.raiz, 0)
        ancho = (contador[0] - 1) * dx + 2 * margen
        alto = (self.altura() - 1) * dy + 2 * margen + 60
        return posiciones, max(ancho, 420), alto

    def graficar_ventana(self):
        """Abre una ventana y dibuja el árbol con círculos y flechas."""
        if self.es_vacio():
            print("El árbol está vacío.")
            return
        try:
            import tkinter as tk
        except ImportError:
            print("tkinter no está disponible; se muestra la versión en texto.")
            self.graficar()
            return

        radio = 24
        posiciones, ancho, alto = self.calcular_posiciones()

        ventana = tk.Tk()
        ventana.title("Árbol Binario de Búsqueda")
        pantalla_w, pantalla_h = ventana.winfo_screenwidth(), ventana.winfo_screenheight()
        lienzo = tk.Canvas(ventana, bg="white", highlightthickness=0,
                           width=min(ancho, pantalla_w - 100),
                           height=min(alto, pantalla_h - 160),
                           scrollregion=(0, 0, ancho, alto))
        if ancho > pantalla_w - 100:         
            barra = tk.Scrollbar(ventana, orient="horizontal", command=lienzo.xview)
            lienzo.configure(xscrollcommand=barra.set)
            barra.pack(side="bottom", fill="x")
        lienzo.pack(fill="both", expand=True)

        lienzo.create_text(ancho / 2, 24, font=("Georgia", 15, "bold"),
                           fill="#333", text="Árbol Binario de Búsqueda")
        lienzo.create_text(ancho / 2, alto - 14, font=("Georgia", 11), fill="#666",
                           text=f"Nodos: {self.contar_nodos()}   |   Altura: {self.altura()}"
                                f"   |   Hojas: {self.contar_hojas()}")

        
        for nodo, (x, y) in posiciones.items():
            for hijo in (nodo.izquierdo, nodo.derecho):
                if hijo is None:
                    continue
                hx, hy = posiciones[hijo]
                largo = ((hx - x) ** 2 + (hy - y) ** 2) ** 0.5
                ux, uy = (hx - x) / largo, (hy - y) / largo
                lienzo.create_line(x + ux * radio, y + uy * radio,
                                   hx - ux * (radio + 2), hy - uy * (radio + 2),
                                   arrow=tk.LAST, arrowshape=(10, 12, 5),
                                   width=2, fill="#222")

       
        for nodo, (x, y) in posiciones.items():
            lienzo.create_oval(x - radio, y - radio, x + radio, y + radio,
                               fill="#F2C14E", outline="#B8860B", width=3)
            lienzo.create_text(x, y, text=str(nodo.dato),
                               font=("Georgia", 14, "bold italic"), fill="#222")

        print("Ventana abierta. Ciérrala para volver al menú.")
        ventana.mainloop()

   
    def pre_orden(self):
        resultado = []
        self._pre_orden(self.raiz, resultado)
        return resultado

    def _pre_orden(self, nodo, res):          
        if nodo is None:
            return
        res.append(nodo.dato)
        self._pre_orden(nodo.izquierdo, res)
        self._pre_orden(nodo.derecho, res)

    def in_orden(self):
        resultado = []
        self._in_orden(self.raiz, resultado)
        return resultado

    def _in_orden(self, nodo, res):          
        if nodo is None:
            return
        self._in_orden(nodo.izquierdo, res)
        res.append(nodo.dato)
        self._in_orden(nodo.derecho, res)

    def post_orden(self):
        resultado = []
        self._post_orden(self.raiz, resultado)
        return resultado

    def _post_orden(self, nodo, res):         
        if nodo is None:
            return
        self._post_orden(nodo.izquierdo, res)
        self._post_orden(nodo.derecho, res)
        res.append(nodo.dato)

    def recorrido_niveles(self):
        """Recorrido por amplitud usando una cola auxiliar."""
        resultado = []
        if self.es_vacio():
            return resultado
        cola = deque([self.raiz])
        while cola:
            actual = cola.popleft()           
            resultado.append(actual.dato)
            if actual.izquierdo:
                cola.append(actual.izquierdo)  
            if actual.derecho:
                cola.append(actual.derecho)
        return resultado

    
    def _busca_mayor(self, nodo):
        while nodo.derecho is not None:
            nodo = nodo.derecho
        return nodo

    def _busca_menor(self, nodo):
        while nodo.izquierdo is not None:
            nodo = nodo.izquierdo
        return nodo

    def eliminar_predecesor(self, x):
        """Elimina x; si tiene dos hijos lo sustituye por el mayor de la izquierda."""
        self.raiz = self._eliminar(x, self.raiz, usar_predecesor=True)

    def eliminar_sucesor(self, x):
        """Elimina x; si tiene dos hijos lo sustituye por el menor de la derecha."""
        self.raiz = self._eliminar(x, self.raiz, usar_predecesor=False)

    def _eliminar(self, x, nodo, usar_predecesor):
        if nodo is None:
            print(f"El valor {x} no está en el árbol.")
            return None
        if x < nodo.dato:
            nodo.izquierdo = self._eliminar(x, nodo.izquierdo, usar_predecesor)
        elif x > nodo.dato:
            nodo.derecho = self._eliminar(x, nodo.derecho, usar_predecesor)
        else:
            # Caso 1 y 2: sin hijos o con un solo hijo
            if nodo.izquierdo is None:
                return nodo.derecho
            if nodo.derecho is None:
                return nodo.izquierdo
            # Caso 3: dos hijos
            if usar_predecesor:
                mayor = self._busca_mayor(nodo.izquierdo)
                nodo.dato = mayor.dato
                nodo.izquierdo = self._eliminar(mayor.dato, nodo.izquierdo, True)
            else:
                menor = self._busca_menor(nodo.derecho)
                nodo.dato = menor.dato
                nodo.derecho = self._eliminar(menor.dato, nodo.derecho, False)
        return nodo

   
    def altura(self):
        return self._altura(self.raiz)

    def _altura(self, nodo):
        if nodo is None:
            return 0
        return 1 + max(self._altura(nodo.izquierdo), self._altura(nodo.derecho))

    def contar_hojas(self):
        return self._contar_hojas(self.raiz)

    def _contar_hojas(self, nodo):
        if nodo is None:
            return 0
        if nodo.izquierdo is None and nodo.derecho is None:
            return 1
        return self._contar_hojas(nodo.izquierdo) + self._contar_hojas(nodo.derecho)

    def contar_nodos(self):
        return self._contar_nodos(self.raiz)

    def _contar_nodos(self, nodo):
        if nodo is None:
            return 0
        return 1 + self._contar_nodos(nodo.izquierdo) + self._contar_nodos(nodo.derecho)

    def es_lleno(self):
        """Lleno: todos los nodos tienen 0 o 2 hijos."""
        return self._es_lleno(self.raiz)

    def _es_lleno(self, nodo):
        if nodo is None:                     
            return True
        if (nodo.izquierdo is None) != (nodo.derecho is None):
            return False                      
        return self._es_lleno(nodo.izquierdo) and self._es_lleno(nodo.derecho)

    def es_completo(self):
        """Completo: todos los niveles llenos salvo el último, que se llena de izquierda a derecha."""
        if self.es_vacio():
            return True
        cola = deque([self.raiz])
        encontro_hueco = False
        while cola:
            actual = cola.popleft()
            for hijo in (actual.izquierdo, actual.derecho):
                if hijo is None:
                    encontro_hueco = True
                else:
                    if encontro_hueco:        
                        return False
                    cola.append(hijo)
        return True

    def eliminar_arbol(self):
        """Poda el árbol completo (Python libera la memoria al perder la referencia)."""
        self._podar(self.raiz)
        self.raiz = None

    def _podar(self, nodo):
        if nodo is None:
            return
        self._podar(nodo.izquierdo)
        self._podar(nodo.derecho)
        nodo.izquierdo = nodo.derecho = None  



def leer_entero(mensaje):
    while True:
        try:
            return int(input(mensaje))
        except ValueError:
            print("Por favor escribe un número entero.")


def mostrar_menu():
    print("""
===== ÁRBOL BINARIO DE BÚSQUEDA =====
 1. Insertar elemento
 2. Mostrar árbol acostado
 3. Buscar un elemento
 4. Recorrido PreOrden
 5. Recorrido InOrden
 6. Recorrido PostOrden
 7. Recorrido por niveles (amplitud)
 8. Eliminar nodo (predecesor)
 9. Eliminar nodo (sucesor)
10. Altura del árbol
11. Cantidad de hojas
12. Cantidad de nodos
13. ¿Es árbol completo?
14. ¿Es árbol lleno?
15. Eliminar todo el árbol
16. Graficar árbol (ventana gráfica)
17. Graficar árbol (texto vertical)
 0. Salir""")


def main():
    arbol = Arbol()
    while True:
        mostrar_menu()
        op = leer_entero("Elige una opción: ")

        if op == 0:
            print("¡Hasta luego!")
            break
        elif op == 1:
            arbol.insertar(leer_entero("Valor a insertar: "))
        elif op == 2:
            arbol.muestra_acostado()
        elif op == 3:
            x = leer_entero("Valor a buscar: ")
            print("Encontrado." if arbol.buscar(x) else "No se encontró.")
        elif op == 4:
            print("PreOrden:", " - ".join(map(str, arbol.pre_orden())))
        elif op == 5:
            print("InOrden:", " - ".join(map(str, arbol.in_orden())))
        elif op == 6:
            print("PostOrden:", " - ".join(map(str, arbol.post_orden())))
        elif op == 7:
            print("Por niveles:", " - ".join(map(str, arbol.recorrido_niveles())))
        elif op == 8:
            arbol.eliminar_predecesor(leer_entero("Valor a eliminar: "))
        elif op == 9:
            arbol.eliminar_sucesor(leer_entero("Valor a eliminar: "))
        elif op == 10:
            print("Altura:", arbol.altura())
        elif op == 11:
            print("Hojas:", arbol.contar_hojas())
        elif op == 12:
            print("Nodos:", arbol.contar_nodos())
        elif op == 13:
            print("Es completo." if arbol.es_completo() else "No es completo.")
        elif op == 14:
            print("Es lleno." if arbol.es_lleno() else "No es lleno.")
        elif op == 15:
            arbol.eliminar_arbol()
            print("Árbol eliminado.")
        elif op == 16:
            arbol.graficar_ventana()
        elif op == 17:
            arbol.graficar()
        else:
            print("Opción no válida.")


if __name__ == "__main__":
    main()