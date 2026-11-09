def encontrar(padre, vertice):
    if padre[vertice] != vertice:
        padre[vertice] = encontrar(padre, padre[vertice])

    return padre[vertice]


def unir(padre, rango, origen, destino):
    raiz1 = encontrar(padre, origen)
    raiz2 = encontrar(padre, destino)

    if raiz1 == raiz2:
        return False

    if rango[raiz1] < rango[raiz2]:
        padre[raiz1] = raiz2

    elif rango[raiz1] > rango[raiz2]:
        padre[raiz2] = raiz1

    else:
        padre[raiz2] = raiz1
        rango[raiz1] += 1

    return True


def kruskal(vertices, aristas):
    padre = {}
    rango = {}

    for vertice in vertices:
        padre[vertice] = vertice
        rango[vertice] = 0

    arbol = []
    costo_total = 0

    # Ordenar las aristas por su peso
    aristas = sorted(aristas, key=lambda x: x[2])

    for origen, destino, peso in aristas:

        if unir(padre, rango, origen, destino):
            arbol.append((origen, destino, peso))
            costo_total += peso

    return arbol, costo_total


# Vértices del grafo
vertices = ['A', 'B', 'C', 'D', 'E']

# Aristas: (origen, destino, peso)
aristas = [
    ('A', 'B', 4),
    ('A', 'C', 2),
    ('B', 'C', 1),
    ('B', 'D', 5),
    ('C', 'D', 8),
    ('C', 'E', 10),
    ('D', 'E', 2)
]

arbol, costo = kruskal(vertices, aristas)

print("ALGORITMO DE KRUSKAL")
print("Aristas seleccionadas:")

for origen, destino, peso in arbol:
    print(origen, "-", destino, "Peso:", peso)

print("Costo total:", costo)