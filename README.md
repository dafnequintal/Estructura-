# Estructura-

En esta actividad realicé dos programas, uno en Java y otro en Python, para trabajar con las ventas mensuales de tres departamentos: Ropa, Deportes y Juguetería.

Utilicé un arreglo bidimensional para organizar la información. El arreglo tiene 12 filas, que corresponden a los meses del año, y 3 columnas, que corresponden a los departamentos. De esta forma, cada posición del arreglo representa las ventas de un departamento durante un mes específico.

En Java utilicé:
int[][] ventas = new int[12][3];

En Python utilicé una lista de listas para representar el arreglo bidimensional:
self.ventas = [[0] * 3 for i in range(12)]

El arreglo empieza con valores en cero porque todavía no se han registrado ventas.

También utilicé arreglos para guardar los nombres de los meses y de los departamentos.
Los meses que utilicé fueron:

- Enero
- Febrero
- Marzo
- Abril
- Mayo
- Junio
- Julio
- Agosto
- Septiembre
- Octubre
- Noviembre
- Diciembre

Los departamentos son:
- Ropa
- Deportes
- Juguetería

Métodos:

Utilicé varios métodos para poder realizar las operaciones que pide la actividad.

Método para insertar una venta
El método `insertarVenta` en Java y `insertar_venta` en Python me permite agregar una cantidad de ventas en un mes y departamento específicos.
Primero selecciono el mes, después selecciono el departamento y finalmente escribo la cantidad de ventas.
El dato se guarda en la posición correspondiente del arreglo bidimensional.

Método para buscar una venta
El método `buscarVenta` en Java y `buscar_venta` en Python me permite consultar una venta que ya se encuentra almacenada.
Para realizar la búsqueda selecciono un mes y un departamento. Después el programa muestra la cantidad de ventas que se encuentra en esa posición.

Método para eliminar una venta
El método `eliminarVenta` en Java y `eliminar_venta` en Python me permite eliminar una venta específica.

Como estoy utilizando un arreglo de tamaño fijo, no elimino físicamente una posición del arreglo. Lo que hago es cambiar el valor de esa posición a cero para indicar que ya no tiene una venta registrada.

Método para mostrar las ventas
También utilicé el método `mostrarVentas` en Java y `mostrar_ventas` en Python.
Este método me permite visualizar todas las ventas registradas en una tabla.
Para recorrer el arreglo utilizo dos ciclos `for`. El primer ciclo recorre los meses y el segundo recorre los departamentos.

Menú

Mi programa cuenta con un menú para facilitar el uso de las funciones.
Las opciones que agregué son:

1. Insertar venta
2. Buscar venta
3. Eliminar venta
4. Mostrar ventas
5. Salir

De esta manera puedo elegir fácilmente la operación que quiero realizar.

Funcionamiento
Primero ejecuto el programa y aparece el menú principal.

Si selecciono la opción 1, puedo registrar una nueva venta.

Si selecciono la opción 2, puedo buscar una venta que ya registré.

Si selecciono la opción 3, puedo eliminar una venta cambiando su valor a cero.

Si selecciono la opción 4, puedo mostrar todas las ventas organizadas por mes y departamento.

La opción 5 me permite salir del programa.

- Ciclos `for` para recorrer el arreglo.
- Condicionales `if` para controlar las diferentes opciones del menú.


