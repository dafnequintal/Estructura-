import random
import time

# Cantidad de alumnos y materias
alumnos = 500
materias = 6

# Nombres de las materias
nombres_materias = [
    "Matematicas",
    "Programacion",
    "Base de Datos",
    "Redes",
    "Ciberseguridad",
    "Ingles"
]

# Crear la matriz
matriz = []

for i in range(alumnos):
    fila = []

    for j in range(materias):
        fila.append(random.randint(0, 10))

    matriz.append(fila)


# Ancho de las columnas
ancho = 18


# Mostrar la tabla
print("=" * (ancho * 7))

print(f"{'Alumno':<{ancho}}", end="")

for materia in nombres_materias:
    print(f"{materia:<{ancho}}", end="")

print()

print("-" * (ancho * 7))


# Mostrar los 500 alumnos
for i in range(alumnos):

    print(f"{'Alumno ' + str(i + 1):<{ancho}}", end="")

    for j in range(materias):
        print(f"{matriz[i][j]:<{ancho}}", end="")

    print()


# Buscar alumno 321 y materia 5
inicio = time.perf_counter()

calificacion = matriz[320][4]

fin = time.perf_counter()

tiempo = fin - inicio


# Mostrar resultado
print()
print("=" * (ancho * 7))

print("BUSQUEDA")
print("=" * (ancho * 7))

print("Alumno:", 321)
print("Materia:", nombres_materias[4])
print("Calificacion:", calificacion)
print("Tiempo de busqueda:", tiempo, "segundos")