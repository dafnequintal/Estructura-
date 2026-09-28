import time


# Fibonacci de forma iterativa
def fibonacci_iterativo(n):
    a = 0
    b = 1

    for i in range(n):
        a, b = b, a + b

    return a


# Fibonacci de forma recursiva
def fibonacci_recursivo(n):
    if n <= 1:
        return n
    else:
        return fibonacci_recursivo(n - 1) + fibonacci_recursivo(n - 2)


# Programa principal
print("===== SERIE DE FIBONACCI =====")

n = int(input("Ingresa la posición de Fibonacci que quieres calcular: "))

# Forma iterativa
inicio = time.perf_counter()
resultado_iterativo = fibonacci_iterativo(n)
fin = time.perf_counter()

tiempo_iterativo = fin - inicio


# Forma recursiva
inicio = time.perf_counter()
resultado_recursivo = fibonacci_recursivo(n)
fin = time.perf_counter()

tiempo_recursivo = fin - inicio


# Resultados
print("\n===== RESULTADOS =====")
print("Número de Fibonacci:", n)
print("Resultado:", resultado_iterativo)

print("\n--- Método iterativo ---")
print("Tiempo de ejecución:", tiempo_iterativo, "segundos")

print("\n--- Método recursivo ---")
print("Tiempo de ejecución:", tiempo_recursivo, "segundos")

