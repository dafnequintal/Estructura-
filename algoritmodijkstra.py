import heapq

def dijkstra(grafo, inicio):
    distancias = {nodo: float('inf') for nodo in grafo}
    anteriores = {nodo: None for nodo in grafo}

    distancias[inicio] = 0
    pendientes = [(0, inicio)]

    while pendientes:
        distancia_actual, nodo_actual = heapq.heappop(pendientes)

        if distancia_actual > distancias[nodo_actual]:
            continue

        for vecino, peso in grafo[nodo_actual]:
            nueva_distancia = distancia_actual + peso

            if nueva_distancia < distancias[vecino]:
                distancias[vecino] = nueva_distancia
                anteriores[vecino] = nodo_actual
                heapq.heappush(pendientes, (nueva_distancia, vecino))

    return distancias, anteriores


def mostrar_camino(anteriores, destino):
    camino = []
    actual = destino

    while actual is not None:
        camino.append(actual)
        actual = anteriores[actual]

    camino.reverse()
    return camino


# Grafo de ejemplo
grafo = {
    'A': [('B', 4), ('C', 2)],
    'B': [('A', 4), ('C', 1), ('D', 5)],
    'C': [('A', 2), ('B', 1), ('D', 8), ('E', 10)],
    'D': [('B', 5), ('C', 8), ('E', 2)],
    'E': [('C', 10), ('D', 2)]
}

inicio = 'A'

distancias, anteriores = dijkstra(grafo, inicio)

print("ALGORITMO DE DIJKSTRA")
print("Punto de inicio:", inicio)

for nodo in grafo:
    camino = mostrar_camino(anteriores, nodo)
    print("Destino:", nodo)
    print("Distancia más corta:", distancias[nodo])
    print("Camino:", " -> ".join(camino))
    print()
    