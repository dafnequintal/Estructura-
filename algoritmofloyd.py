def floyd(matriz):
    n = len(matriz)

    distancias = [fila[:] for fila in matriz]

    for k in range(n):
        for i in range(n):
            for j in range(n):

                nueva_distancia = distancias[i][k] + distancias[k][j]

                if nueva_distancia < distancias[i][j]:
                    distancias[i][j] = nueva_distancia

    return distancias


# Matriz de ejemplo
INF = float('inf')

grafo = [
    [0,   5,   INF, 10],
    [INF, 0,   3,   INF],
    [INF, INF, 0,   1],
    [INF, INF, INF, 0]
]

resultado = floyd(grafo)

print("ALGORITMO DE FLOYD")
print("Matriz de distancias más cortas:")

for fila in resultado:
    print(fila)