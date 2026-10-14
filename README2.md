## 🧩 Métodos que maneja el programa

### 📄 `hanoi.py` → clase `TorreHanoi`: **8 métodos**

| # | Método | Descripción |
|---|--------|-------------|
| 1 | `__init__(n)` | Crea las torres A, B y C y coloca los `n` discos en A |
| 2 | `mover_disco(origen, destino)` | Mueve el disco superior de una torre a otra y cuenta el movimiento |
| 3 | `resolver(n, origen, auxiliar, destino)` | Algoritmo recursivo principal de la Torre de Hanoi |
| 4 | `contar_movimientos(n)` | Recursión que solo cuenta los movimientos (2ⁿ − 1) |
| 5 | `dibujar()` | Dibuja las torres en la terminal con un color por disco |
| 6 | `resolver_con_tiempo()` | Resuelve el juego y mide el tiempo con `time.perf_counter()` |
| 7 | `formatear_tiempo(seg)` | Convierte segundos a minutos, horas, días o años |
| 8 | `estimar_tiempo(n, seg_por_mov)` | Estima el tiempo para valores grandes de `n` |

Funciones auxiliares fuera de la clase: `color()`, `benchmark()` y `main()`.

### 🎮 `hanoi_juego.py` → clase `JuegoHanoi`: **11 métodos**

| # | Método | Descripción |
|---|--------|-------------|
| 1 | `__init__(root)` | Crea la ventana, el botón Reset, el deslizador de discos, los contadores y el lienzo |
| 2 | `reiniciar()` | Reinicia la partida con el número de discos elegido |
| 3 | `torre_en(x)` | Indica sobre qué torre (0, 1 o 2) está la posición del mouse |
| 4 | `mover(a, b)` | Valida y realiza el movimiento de un disco; detecta si se ganó |
| 5 | `al_presionar(e)` | Evento de clic: levanta un disco o lo suelta en otra torre |
| 6 | `al_arrastrar(e)` | Evento de arrastre: mueve el disco junto con el mouse |
| 7 | `al_soltar(e)` | Evento al soltar el botón: deja el disco en la torre destino |
| 8 | `ancho_disco(d)` | Calcula el ancho de un disco según su tamaño |
| 9 | `rect_disco(cx, y_base, d)` | Calcula las coordenadas del rectángulo de un disco |
| 10 | `dibujar()` | Redibuja torres, discos y contadores en pantalla |
| 11 | `pintar(cx, y, d, sombra)` | Dibuja un disco con su color (y su sombra si está levantado) |
