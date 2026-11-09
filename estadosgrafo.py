from itertools import permutations
import heapq
import tkinter as tk
from tkinter import ttk

# 1. ESTADOS DE LA REPUBLICA
ESTADOS = [
    "Yucatán", "Quintana Roo", "Campeche",
    "Tabasco", "Chiapas", "Veracruz", "Oaxaca"
]

# 2. RELACIONES Y COSTOS DE TRASLADO
RELACIONES = [
    ("Yucatán", "Quintana Roo", 550),
    ("Yucatán", "Campeche", 350),
    ("Quintana Roo", "Campeche", 650),
    ("Campeche", "Tabasco", 600),
    ("Tabasco", "Chiapas", 550),
    ("Tabasco", "Veracruz", 900),
    ("Chiapas", "Oaxaca", 1000),
    ("Veracruz", "Oaxaca", 800),
]

# 3. CREAR EL GRAFO
GRAFO = {e: {} for e in ESTADOS}

for a, b, c in RELACIONES:
    GRAFO[a][b] = c
    GRAFO[b][a] = c


# 4. MOSTRAR ESTADOS Y RELACIONES
def mostrar_relaciones():
    print("=" * 60)
    print("ESTADOS Y SUS RELACIONES (COSTOS EN PESOS)")
    print("=" * 60)

    for e, vecinos in GRAFO.items():
        print(f"- {e}: " + ", ".join(
            f"{v} (${c})" for v, c in vecinos.items()
        ))

    print("\nLISTA DE CONEXIONES:")

    for a, b, c in RELACIONES:
        print(f"{a} <-> {b}: ${c}")


# 5. ALGORITMO DE DIJKSTRA
def dijkstra(origen, destino):

    cola = [(0, origen, [origen])]
    visitados = set()

    while cola:
        costo, nodo, camino = heapq.heappop(cola)

        if nodo == destino:
            return camino, costo

        if nodo in visitados:
            continue

        visitados.add(nodo)

        for vecino, c in GRAFO[nodo].items():
            if vecino not in visitados:
                heapq.heappush(
                    cola,
                    (costo + c, vecino, camino + [vecino])
                )

    return None, float("inf")


# 6. RECORRIDO SIN REPETIR ESTADOS
def recorrido_sin_repetir():

    mejor = None
    mejor_costo = float("inf")

    for orden in permutations(ESTADOS):

        if all(
            orden[i + 1] in GRAFO[orden[i]]
            for i in range(6)
        ):

            costo = sum(
                GRAFO[orden[i]][orden[i + 1]]
                for i in range(6)
            )

            if costo < mejor_costo:
                mejor = list(orden)
                mejor_costo = costo

    return mejor, mejor_costo


# 7. RECORRIDO REPITIENDO ESTADOS
def recorrido_con_repeticion():

    mejor = None
    mejor_costo = float("inf")

    for orden in permutations(ESTADOS):

        camino = [orden[0]]
        costo = 0

        for i in range(6):

            tramo, c = dijkstra(
                orden[i], orden[i + 1]
            )

            camino += tramo[1:]
            costo += c

        if (
            len(camino) != len(set(camino))
            and costo < mejor_costo
        ):

            mejor = camino
            mejor_costo = costo

    return mejor, mejor_costo


# 8. MOSTRAR DETALLE DEL RECORRIDO
def detalle(camino):

    for i in range(len(camino) - 1):

        a = camino[i]
        b = camino[i + 1]

        print(
            f"     {a} -> {b}: ${GRAFO[a][b]}"
        )


# 9. POSICIONES DE LOS ESTADOS EN EL GRAFO
POS = {
    "Yucatán": (560, 90),
    "Quintana Roo": (780, 200),
    "Campeche": (480, 250),
    "Tabasco": (330, 360),
    "Chiapas": (420, 520),
    "Veracruz": (140, 260),
    "Oaxaca": (150, 500),
}


# 10. DIBUJAR EL GRAFO
def dibujar_en(canvas, titulo, camino=None, costo=None):

    canvas.create_text(
        450, 25,
        text=titulo,
        font=("Arial", 14, "bold")
    )

    aristas_rojas = set()

    if camino:
        for i in range(len(camino) - 1):
            aristas_rojas.add(
                frozenset((camino[i], camino[i + 1]))
            )

    # Dibujar conexiones y costos
    for a, b, c in RELACIONES:

        x1, y1 = POS[a]
        x2, y2 = POS[b]

        roja = frozenset((a, b)) in aristas_rojas

        canvas.create_line(
            x1, y1, x2, y2,
            width=5 if roja else 2,
            fill="red" if roja else "gray"
        )

        mx = (x1 + x2) / 2
        my = (y1 + y2) / 2

        texto = canvas.create_text(
            mx, my,
            text=f"${c}",
            font=("Arial", 11, "bold"),
            fill="blue"
        )

        x0, y0, xf, yf = canvas.bbox(texto)

        fondo = canvas.create_rectangle(
            x0 - 3, y0 - 1,
            xf + 3, yf + 1,
            fill="white",
            outline="#cccccc"
        )

        canvas.tag_raise(texto, fondo)

    # Dibujar los estados
    for e, (x, y) in POS.items():

        canvas.create_oval(
            x - 48, y - 28,
            x + 48, y + 28,
            fill="#9ecae1",
            outline="black",
            width=2
        )

        canvas.create_text(
            x, y,
            text=e,
            font=("Arial", 10, "bold")
        )

    # Mostrar recorrido y costo total
    if camino:

        canvas.create_text(
            450, 575,
            text=f"COSTO TOTAL: ${costo:,} MXN",
            font=("Arial", 15, "bold"),
            fill="green"
        )

        canvas.create_text(
            450, 615,
            text=" -> ".join(camino),
            font=("Arial", 9),
            width=860
        )


# 11. CREAR VENTANA CON TRES PESTAÑAS
def dibujar(c1, costo1, c2, costo2):

    ventana = tk.Tk()
    ventana.title("Grafo de 7 estados de México")

    pestañas = ttk.Notebook(ventana)
    pestañas.pack(fill="both", expand=True)

    resultados = [
        ("Grafo completo (pesos MXN)", None, None),
        ("a) Sin repetir estados", c1, costo1),
        ("b) Repitiendo estados", c2, costo2)
    ]

    for titulo, camino, costo in resultados:

        marco = tk.Frame(pestañas)

        canvas = tk.Canvas(
            marco,
            width=900,
            height=650,
            bg="white"
        )

        canvas.pack()

        dibujar_en(
            canvas,
            titulo,
            camino,
            costo
        )

        pestañas.add(marco, text=titulo)

    ventana.mainloop()


# 12. PROGRAMA PRINCIPAL
def main():

    mostrar_relaciones()

    # INCISO A
    c1, costo1 = recorrido_sin_repetir()

    print("\n" + "=" * 60)
    print("A) RECORRIDO SIN REPETIR ESTADOS")
    print("=" * 60)

    if c1:
        print(" -> ".join(c1))
        detalle(c1)
        print(f"COSTO TOTAL: ${costo1}")

    else:
        print("No se encontró un recorrido válido.")

    # INCISO B
    c2, costo2 = recorrido_con_repeticion()

    print("\n" + "=" * 60)
    print("B) RECORRIDO REPITIENDO ESTADOS")
    print("=" * 60)

    if c2:
        print(" -> ".join(c2))
        detalle(c2)

        rep = sorted({
            e for e in c2 if c2.count(e) > 1
        })

        print("Estados repetidos:", ", ".join(rep))
        print(f"COSTO TOTAL: ${costo2}")

    else:
        print("No se encontró un recorrido válido.")

    # RESUMEN DE COSTOS
    print("\n" + "=" * 60)
    print("RESUMEN DE COSTOS TOTALES")
    print("=" * 60)

    print(f"Inciso a): ${costo1}")
    print(f"Inciso b): ${costo2}")

    # MOSTRAR GRAFO
    try:
        dibujar(c1, costo1, c2, costo2)

    except Exception as e:
        print("No se pudo abrir la ventana:", e)


if __name__ == "__main__":
    main()