def warshall(matriz):
    n = len(matriz)

    alcance = [fila[:] for fila in matriz]

    for k in range(n):
        for i in range(n):
            for j in range(n):

                if alcance[i][k] == 1 and alcance[k][j] == 1:
                    alcance[i][j] = 1

    return alcance


# Matriz de conexiones
grafo = [
    [0, 1, 0, 0],
    [0, 0, 1, 0],
    [0, 0, 0, 1],
    [0, 0, 0, 0]
]

resultado = warshall(grafo)

print("ALGORITMO DE WARSHALL")
print("Matriz de conectividad:")

for fila in resultado:
    print(fila)