
CAPACIDAD = 20 


class NodoIngrediente:
    def __init__(self, nombre):
        self.nombre = nombre
        self.sig = None 


class ListaIngredientes:
    def __init__(self):
        self.cabeza = None

    def vacia(self):
        return self.cabeza is None

    def existe(self, nombre):
        actual = self.cabeza
        while actual is not None:
            if actual.nombre.lower() == nombre.lower():
                return True
            actual = actual.sig
        return False

    def insertar(self, nombre):
        """Inserta al final. Regresa False si ya existe (evita repetidos)."""
        if self.existe(nombre):
            return False
        nuevo = NodoIngrediente(nombre)
        if self.cabeza is None:
            self.cabeza = nuevo
        else:
            actual = self.cabeza
            while actual.sig is not None:
                actual = actual.sig
            actual.sig = nuevo
        return True

    def eliminar(self, nombre):
        """Elimina un ingrediente. Regresa False si no se encontró."""
        nombre = nombre.strip()
        anterior, actual = None, self.cabeza
        while actual is not None:
            if actual.nombre.lower() == nombre.lower():
                if anterior is None:
                    self.cabeza = actual.sig
                else:
                    anterior.sig = actual.sig
                return True
            anterior, actual = actual, actual.sig
        return False

    def como_lista(self):
        res, actual = [], self.cabeza
        while actual is not None:
            res.append(actual.nombre)
            actual = actual.sig
        return res

    def fusionar(self, otra):
        """Pasa a esta lista los ingredientes de 'otra' que no existan aún."""
        nuevos = 0
        for ing in otra.como_lista():
            if self.insertar(ing):
                nuevos += 1
        return nuevos

    def __str__(self):
        return " -> ".join(self.como_lista() + ["NIL"])



class Registro:
    def __init__(self, nombre, ingredientes=None):
        self.nombre = nombre
        self.ingredientes = ingredientes if ingredientes else ListaIngredientes()


class Postres:
    def __init__(self, capacidad=CAPACIDAD):
        self.arreglo = [None] * capacidad
        self.n = 0  

    
    def buscar(self, nombre):
        bajo, alto = 0, self.n - 1
        clave = nombre.strip().lower()
        while bajo <= alto:
            medio = (bajo + alto) // 2
            actual = self.arreglo[medio].nombre.lower()
            if actual == clave:
                return True, medio
            if actual < clave:
                bajo = medio + 1
            else:
                alto = medio - 1
        return False, bajo


    def imprimir_ingredientes(self, nombre):
        if self.n == 0:
            print("Error: la estructura POSTRES está vacía.")
            return
        ok, i = self.buscar(nombre)
        if not ok:
            print(f"Error: el postre '{nombre}' no existe.")
            return
        lista = self.arreglo[i].ingredientes
        if lista.vacia():
            print(f"El postre '{self.arreglo[i].nombre}' no tiene ingredientes (NIL).")
        else:
            print(f"Ingredientes de '{self.arreglo[i].nombre}': {lista}")

   
    def insertar_ingredientes(self, nombre, ingredientes):
        ok, i = self.buscar(nombre)
        if not ok:
            print(f"Error: el postre '{nombre}' no existe.")
            return
        for ing in ingredientes:
            if not ing.strip():
                print("  Aviso: se ignoró un ingrediente vacío.")
            elif self.arreglo[i].ingredientes.insertar(ing.strip()):
                print(f"  '{ing.strip()}' insertado.")
            else:
                print(f"  Aviso: '{ing.strip()}' ya estaba en la lista (no se repite).")

    
    def eliminar_ingrediente(self, nombre, ingrediente):
        ok, i = self.buscar(nombre)
        if not ok:
            print(f"Error: el postre '{nombre}' no existe.")
            return
        lista = self.arreglo[i].ingredientes
        if lista.vacia():
            print("Error: la lista de ingredientes está vacía.")
        elif lista.eliminar(ingrediente):
            print(f"Ingrediente '{ingrediente}' eliminado.")
        else:
            print(f"Error: '{ingrediente}' no está en la lista de '{nombre}'.")

    
    def alta(self, nombre, ingredientes, permitir_repetido=False):
        nombre = nombre.strip()
        if not nombre:
            print("Error: el nombre no puede estar vacío.")
            return False
        if self.n == len(self.arreglo):
            print("Error: el arreglo está lleno (desbordamiento).")
            return False
        ok, i = self.buscar(nombre)
        if ok and not permitir_repetido:
            print(f"Error: el postre '{nombre}' ya existe.")
            return False
        if ok:  
            while i < self.n and self.arreglo[i].nombre.lower() == nombre.lower():
                i += 1
        lista = ListaIngredientes()
        for ing in ingredientes:
            if ing.strip():
                lista.insertar(ing.strip())
        for k in range(self.n, i, -1):  
            self.arreglo[k] = self.arreglo[k - 1]
        self.arreglo[i] = Registro(nombre, lista)
        self.n += 1
        print(f"Postre '{nombre}' dado de alta.")
        return True

   
    def baja(self, nombre):
        if self.n == 0:
            print("Error: la estructura POSTRES está vacía.")
            return
        ok, i = self.buscar(nombre)
        if not ok:
            print(f"Error: el postre '{nombre}' no existe.")
            return
        for k in range(i, self.n - 1):  
            self.arreglo[k] = self.arreglo[k + 1]
        self.arreglo[self.n - 1] = None
        self.n -= 1
        print(f"Postre '{nombre}' dado de baja junto con todos sus ingredientes.")

    
    def eliminar_repetidos(self):
        if self.n == 0:
            print("Error: la estructura POSTRES está vacía.")
            return
        escritura = 0
        eliminados = 0
        for lectura in range(1, self.n):
            base = self.arreglo[escritura]
            actual = self.arreglo[lectura]
            if actual.nombre.lower() == base.nombre.lower():
                nuevos = base.ingredientes.fusionar(actual.ingredientes)
                eliminados += 1
                print(f"Repetido: '{actual.nombre}'. Su lista se fusionó con la "
                      f"original ({nuevos} ingredientes nuevos) y luego se descartó.")
            else:
                escritura += 1
                self.arreglo[escritura] = actual
        for k in range(escritura + 1, self.n):
            self.arreglo[k] = None
        self.n = escritura + 1
        if eliminados == 0:
            print("Mensaje: no se encontraron postres repetidos.")
        else:
            print(f"Se eliminaron {eliminados} elemento(s) repetido(s).")

    def mostrar_todo(self):
        if self.n == 0:
            print("POSTRES está vacío.")
            return
        for i in range(self.n):
            r = self.arreglo[i]
            print(f"[{i}] {r.nombre}: {r.ingredientes}")



def pedir_ingredientes():
    txt = input("Ingredientes separados por coma: ")
    return [x for x in txt.split(",")]


def main():
    p = Postres()
    
    p.alta("Roles", ["harina", "canela", "mantequilla", "azúcar", "levadura"])
    p.alta("Galletas chocohip", ["harina", "mantequilla", "azúcar", "huevo", "chispas de chocolate"])
    p.alta("Pan de zanahoria", ["zanahoria", "harina", "huevo", "azúcar", "aceite", "nuez"])

    menu = """
===== POSTRES =====
1. Imprimir ingredientes de un postre
2. Insertar ingredientes a un postre
3. Eliminar un ingrediente de un postre
4. Alta de postre
5. Baja de postre
6. Eliminar postres repetidos (ejercicio 2)
7. Alta de postre repetido SIN validar (sólo para probar el ejercicio 2)
8. Mostrar toda la estructura
0. Salir
Opción: """
    while True:
        op = input(menu).strip()
        if op == "0":
            break
        elif op == "1":
            p.imprimir_ingredientes(input("Postre: "))
        elif op == "2":
            nombre = input("Postre: ")
            p.insertar_ingredientes(nombre, pedir_ingredientes())
        elif op == "3":
            p.eliminar_ingrediente(input("Postre: "), input("Ingrediente a eliminar: "))
        elif op == "4":
            p.alta(input("Nombre del postre: "), pedir_ingredientes())
        elif op == "5":
            p.baja(input("Postre: "))
        elif op == "6":
            p.eliminar_repetidos()
        elif op == "7":
            p.alta(input("Nombre del postre: "), pedir_ingredientes(), permitir_repetido=True)
        elif op == "8":
            p.mostrar_todo()
        else:
            print("Opción no válida.")


if __name__ == "__main__":
    main()