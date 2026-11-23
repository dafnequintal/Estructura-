"""
Ejercicio 1: Intercalacion de dos listas ya ordenadas
Materia: Estructura de Datos
Alumna: Dafne Andrea Quintal Medina

Problema: dos grupos de la misma materia entregaron su lista de
calificaciones ya ordenada de menor a mayor. Se necesita una sola
lista general, tambien ordenada, sin volver a ordenar todo desde cero.
"""


def intercalar(lista_a, lista_b, mostrar_pasos=False):
    """Mezcla dos listas ordenadas por calificacion en una sola lista.
    Cada elemento es una tupla: (nombre, calificacion)."""
    resultado = []
    i = 0  
    j = 0  

    
    while i < len(lista_a) and j < len(lista_b):
        alumno_a = lista_a[i]
        alumno_b = lista_b[j]
        
        if alumno_a[1] <= alumno_b[1]:
            resultado.append(alumno_a)
            i += 1
            elegido = "A"
        else:
            resultado.append(alumno_b)
            j += 1
            elegido = "B"
        if mostrar_pasos:
            print(f"  Comparo {alumno_a[1]} (A) con {alumno_b[1]} (B)"
                  f" -> paso el del grupo {elegido}")

    
    while i < len(lista_a):
        resultado.append(lista_a[i])
        i += 1
    while j < len(lista_b):
        resultado.append(lista_b[j])
        j += 1

    return resultado


def esta_ordenada(lista):
    """Revisa que las calificaciones queden de menor a mayor."""
    for k in range(len(lista) - 1):
        if lista[k][1] > lista[k + 1][1]:
            return False
    return True


def mostrar_lista(titulo, lista):
    print(titulo)
    for posicion, (nombre, calificacion) in enumerate(lista, start=1):
        print(f"  {posicion:2d}. {nombre:<14} {calificacion}")



if __name__ == "__main__":
    
    grupo_a = [("Ana Perez", 68), ("Luis Mena", 75), ("Sofia Cruz", 82),
               ("Diego Pech", 90), ("Marta Uc", 95)]
    grupo_b = [("Jorge Chan", 60), ("Karla May", 75), ("Raul Tun", 80),
               ("Elena Canul", 88), ("Pedro Cauich", 93),
               ("Rosa Euan", 100)]

    mostrar_lista("Grupo A (ordenado):", grupo_a)
    mostrar_lista("Grupo B (ordenado):", grupo_b)

    print("\nProceso de intercalacion:")
    lista_general = intercalar(grupo_a, grupo_b, mostrar_pasos=True)

    print()
    mostrar_lista("Lista general (resultado):", lista_general)
    print("\n¿Quedo ordenada?", esta_ordenada(lista_general))