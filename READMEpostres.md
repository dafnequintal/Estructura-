# Postres: arreglo de listas ligadas en Python

Programa que maneja la estructura `POSTRES`: un arreglo ordenado alfabéticamente donde cada elemento guarda el nombre de un postre y una lista ligada con sus ingredientes.

## Estructura de datos

```
POSTRES[0] -> Galletas chocohip -> harina -> mantequilla -> ... -> NIL
POSTRES[1] -> Pan de zanahoria  -> zanahoria -> harina -> ... -> NIL
POSTRES[2] -> Roles             -> harina -> canela -> ... -> NIL
```

- Arreglo de tamaño fijo (20), ordenado, con búsqueda binaria.
- Lista ligada simple de ingredientes, que termina en `NIL` (`None`).

## Ejercicio 1

| Opción | Operación | Casos verificados |
|---|---|---|
| 1 | Imprimir ingredientes | Arreglo vacío, postre inexistente, lista vacía |
| 2 | Insertar ingredientes | Postre inexistente, ingrediente vacío, ingrediente repetido |
| 3 | Eliminar ingrediente | Postre inexistente, lista vacía, ingrediente inexistente |
| 4 | Alta de postre | Nombre vacío, arreglo lleno, postre ya existente |
| 5 | Baja de postre | Arreglo vacío, postre inexistente |

## Ejercicio 2: eliminar repetidos

La opción 6 ejecuta `eliminar_repetidos()`. Como el arreglo está ordenado, los repetidos quedan juntos y se eliminan con un solo recorrido. La opción 7 permite dar de alta un postre repetido sin validar, solo para poder probarlo.

### ¿Qué sucedió con las listas?

Al eliminar un elemento repetido del arreglo, su lista de ingredientes no se elimina automáticamente: es una estructura independiente, enlazada al arreglo solo por una referencia. Si únicamente se recorren los elementos del arreglo, la lista del repetido queda sin referencia y sus ingredientes se pierden, aunque no estuvieran en la lista del postre original.

Para evitarlo, el subprograma fusiona primero la lista del repetido con la del original, sin duplicar ingredientes, y después descarta el elemento. No se genera ningún error cuando hay repetidos. Se muestran mensajes informativos, y solo se muestra error si el arreglo está vacío.

### Conclusiones

1. Un arreglo de listas ligadas combina estructuras estáticas y dinámicas. Operar sobre el arreglo no modifica automáticamente las listas, así que hay que decidir qué hacer con ellas.
2. Mantener el arreglo ordenado permite usar búsqueda binaria (O(log n)) y eliminar repetidos en un solo recorrido, ya que quedan adyacentes. A cambio, las altas y bajas requieren recorrer elementos (O(n)).
3. Descartar el elemento repetido sin más pierde información. Fusionar las listas conserva todos los ingredientes y evita repeticiones.
4. Es indispensable validar los casos límite (arreglo vacío o lleno, elemento inexistente, lista vacía, datos repetidos o vacíos) para que el programa no falle y el usuario reciba mensajes claros.
5. Prevenir duplicados desde el alta es más sencillo que eliminarlos después. Aun así, el subprograma es necesario cuando los datos llegan de otra fuente o ya contienen repetidos.
