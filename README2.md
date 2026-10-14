# Torre de Hanoi en Python

Programa de la Torre de Hanoi hecho en Python con `tkinter`. Se puede jugar con el mouse y también mide cuánto tarda en resolverse con 5, 10, 30 y 64 discos.

## Cómo ejecutarlo

```
python hanoi_juego.py
```

- Haz clic en una torre para levantar su disco de arriba y otro clic en la torre donde lo quieres poner. También se puede arrastrar.
- Un disco grande no se puede poner sobre uno más pequeño.
- El deslizador cambia el número de discos (de 1 a 8) y el botón Reset reinicia la partida.
- El botón **Medir tiempos** abre una ventana que resuelve el juego con 5, 10, 30 y 64 discos y muestra cuánto tarda.

## Métodos que maneja

El programa tiene una clase llamada `JuegoHanoi` con **20 métodos**.

**Métodos del juego (11):**

- `__init__`: crea la ventana, el botón Reset, el deslizador, los contadores y el lienzo.
- `reiniciar`: empieza una partida nueva con el número de discos elegido.
- `torre_en`: dice sobre qué torre está el mouse.
- `mover`: revisa que el movimiento sea válido, lo hace y checa si ya ganaste.
- `al_presionar`: se activa con el clic, levanta el disco o lo suelta.
- `al_arrastrar`: mueve el disco mientras se arrastra el mouse.
- `al_soltar`: deja el disco en la torre donde se suelta el mouse.
- `ancho_disco`: calcula qué tan ancho es cada disco.
- `rect_disco`: calcula las coordenadas del rectángulo de cada disco.
- `dibujar`: vuelve a dibujar torres, discos y contadores.
- `pintar`: dibuja un disco con su color.

**Métodos de la medición de tiempos (9):**

- `resolver_recursivo`: resuelve el juego con recursión moviendo los discos.
- `resolver_medido`: resuelve con n discos y devuelve los movimientos y el tiempo que tardó.
- `formatear_tiempo`: pasa los segundos a minutos, horas, días o años.
- `estimar_tiempo`: calcula cuánto tardaría con muchos discos sin ejecutarlo completo.
- `medir_tiempos`: abre la ventana de medición.
- `cerrar_medicion`: cierra esa ventana.
- `escribir`: agrega una línea de resultados en la ventana.
- `iniciar_hilo`: lanza la medición en segundo plano para que el programa no se congele.
- `trabajo_medicion`: hace las mediciones de 5, 10, 30 y 64 discos y escribe la tabla.

## Tiempos de ejecución

Medí el tiempo con `time.perf_counter()`. Estos son los resultados:

| Discos | Movimientos | Tiempo | Tipo |
|--------|-------------|--------|------|
| 5 | 31 | 0.00005 s | medido |
| 10 | 1,023 | 0.0002 s | medido |
| 30 | 1,073,741,823 | aprox. 5 minutos | estimado |
| 64 | 18,446,744,073,709,551,615 | aprox. 164,000 años | estimado |

Con 5 y 10 discos el programa se ejecutó completo y el tiempo es real. Con 64 discos es imposible ejecutarlo completo, así que lo estimé: medí cuánto tarda un movimiento con 20 discos (aprox. 281 nanosegundos) y lo multipliqué por el total de movimientos (2^n - 1). Con 30 discos se puede ejecutar completo marcando la casilla de la ventana, y tarda alrededor de 5 minutos.

Los tiempos cambian según la computadora, pero la proporción entre ellos es la misma.

## Conclusiones

- El número de movimientos es 2^n - 1, así que cada disco que se agrega duplica el trabajo.
- Con 5 y 10 discos el programa termina casi al instante, con 30 ya tarda varios minutos y con 64 tardaría más de 160 mil años.
- El algoritmo recursivo ya usa el mínimo de movimientos posible, así que no se puede hacer más rápido. El problema es lento por sí mismo, no por cómo está escrito el código.
- La parte recursiva es muy corta (pocas líneas), pero eso no significa que sea rápida: un programa corto puede tardar muchísimo si el problema crece de forma exponencial.
- Dibujar cada paso en pantalla hace todo mucho más lento, por eso al medir los tiempos no se dibuja nada.
- Cuando no se puede ejecutar algo completo, se puede estimar el resultado midiendo casos pequeños, como hice con 64 discos.
