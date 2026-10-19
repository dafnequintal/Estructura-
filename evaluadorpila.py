"""
Ejercicio 1: Evaluador de expresiones aritméticas en notación posfija y prefija
usando una pila.

Los elementos (operandos y operadores) deben ir separados por espacios.
Ejemplos:
    Posfija: 3 4 + 2 *      -> 14
    Prefija: * + 3 4 2      -> 14
"""


class Pila:
    """Implementación de una pila (LIFO) usando una lista de Python."""

    def __init__(self):
        self.__items = []

    def apilar(self, elemento):
        """Agrega un elemento en la cima de la pila."""
        self.__items.append(elemento)

    def desapilar(self):
        """Quita y devuelve el elemento de la cima."""
        if self.esta_vacia():
            raise IndexError("La pila está vacía")
        return self.__items.pop()

    def cima(self):
        """Devuelve el elemento de la cima sin quitarlo."""
        if self.esta_vacia():
            raise IndexError("La pila está vacía")
        return self.__items[-1]

    def esta_vacia(self):
        return len(self.__items) == 0

    def tamanio(self):
        return len(self.__items)


# Operadores soportados
OPERADORES = {"+", "-", "*", "/", "^"}


def aplicar_operador(operador, a, b):
    """Calcula 'a operador b'."""
    if operador == "+":
        return a + b
    if operador == "-":
        return a - b
    if operador == "*":
        return a * b
    if operador == "/":
        if b == 0:
            raise ZeroDivisionError("División entre cero")
        return a / b
    if operador == "^":
        return a ** b
    raise ValueError(f"Operador desconocido: {operador}")


def convertir_numero(token):
    """Convierte un token a número; lanza error si no es válido."""
    try:
        return float(token)
    except ValueError:
        raise ValueError(f"Token inválido: '{token}'")


def evaluar_posfija(expresion):
    """
    Evalúa una expresión posfija.
    Se recorre de IZQUIERDA a DERECHA:
      - Operando  -> se apila.
      - Operador  -> se desapilan dos operandos (primero b, luego a),
                     se calcula a operador b y se apila el resultado.
    """
    tokens = expresion.split()
    if not tokens:
        raise ValueError("La expresión está vacía")

    pila = Pila()
    for token in tokens:
        if token in OPERADORES:
            if pila.tamanio() < 2:
                raise ValueError("Expresión inválida: faltan operandos")
            b = pila.desapilar()
            a = pila.desapilar()
            pila.apilar(aplicar_operador(token, a, b))
        else:
            pila.apilar(convertir_numero(token))

    if pila.tamanio() != 1:
        raise ValueError("Expresión inválida: sobran operandos")
    return pila.desapilar()


def evaluar_prefija(expresion):
    """
    Evalúa una expresión prefija.
    Se recorre de DERECHA a IZQUIERDA:
      - Operando  -> se apila.
      - Operador  -> se desapilan dos operandos (primero a, luego b),
                     se calcula a operador b y se apila el resultado.
    """
    tokens = expresion.split()
    if not tokens:
        raise ValueError("La expresión está vacía")

    pila = Pila()
    for token in reversed(tokens):
        if token in OPERADORES:
            if pila.tamanio() < 2:
                raise ValueError("Expresión inválida: faltan operandos")
            a = pila.desapilar()
            b = pila.desapilar()
            pila.apilar(aplicar_operador(token, a, b))
        else:
            pila.apilar(convertir_numero(token))

    if pila.tamanio() != 1:
        raise ValueError("Expresión inválida: sobran operandos")
    return pila.desapilar()


def formatear(resultado):
    """Muestra enteros sin decimales (14.0 -> 14)."""
    if resultado == int(resultado):
        return str(int(resultado))
    return str(round(resultado, 4))


def menu():
    print("=" * 50)
    print(" EVALUADOR DE EXPRESIONES (POSFIJA / PREFIJA)")
    print("=" * 50)
    print("Operadores válidos: + - * / ^")
    print("Separa cada elemento con un espacio.\n")

    while True:
        print("\n1. Evaluar expresión posfija  (ej: 3 4 + 2 *)")
        print("2. Evaluar expresión prefija  (ej: * + 3 4 2)")
        print("3. Salir")
        opcion = input("Elige una opción: ").strip()

        if opcion == "3":
            print("¡Hasta luego!")
            break
        if opcion not in ("1", "2"):
            print("Opción no válida.")
            continue

        expresion = input("Escribe la expresión: ")
        try:
            if opcion == "1":
                resultado = evaluar_posfija(expresion)
            else:
                resultado = evaluar_prefija(expresion)
            print(f"Resultado: {formatear(resultado)}")
        except (ValueError, ZeroDivisionError) as error:
            print(f"Error: {error}")


if __name__ == "__main__":
    menu()