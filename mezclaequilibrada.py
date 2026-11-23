"""
Ejercicio 3: Mezcla equilibrada
Materia: Estructura de Datos
Alumna: Dafne Andrea Quintal Medina

Problema: una cadena de papelerias guarda los montos de sus ventas del
dia sin orden. Se quieren ordenar de menor a mayor usando 4 archivos
auxiliares (2 de entrada y 2 de salida) que se intercambian el papel
en cada pasada. Los archivos se simulan con listas; cada archivo es
una lista de "corridas" (pedazos que ya estan ordenados).
"""


def ordenar_por_insercion(bloque):
    """Ordenamiento interno sencillo (insercion) para un bloque chico
    que si cabe en memoria. No se usa sort() ni sorted()."""
    lista = bloque[:] 
    for i in range(1, len(lista)):
        valor = lista[i]
        k = i - 1
        while k >= 0 and lista[k] > valor:
            lista[k + 1] = lista[k]
            k -= 1
        lista[k + 1] = valor
    return lista


def crear_corridas(datos, tamano_corrida):
    """Parte los datos en bloques, ordena cada uno y regresa la lista
    de corridas."""
    corridas = []
    for inicio in range(0, len(datos), tamano_corrida):
        bloque = datos[inicio:inicio + tamano_corrida]
        corridas.append(ordenar_por_insercion(bloque))
    return corridas


def repartir_corridas(corridas):
    """Reparte las corridas de forma alternada en dos archivos."""
    archivo_1 = []
    archivo_2 = []
    for numero, corrida in enumerate(corridas):
        if numero % 2 == 0:
            archivo_1.append(corrida)
        else:
            archivo_2.append(corrida)
    return archivo_1, archivo_2


def mezclar_corridas(corrida_x, corrida_y):
    """Mezcla dos corridas ordenadas en una sola corrida ordenada."""
    resultado = []
    i = 0
    j = 0
    while i < len(corrida_x) and j < len(corrida_y):
        if corrida_x[i] <= corrida_y[j]:
            resultado.append(corrida_x[i])
            i += 1
        else:
            resultado.append(corrida_y[j])
            j += 1
    while i < len(corrida_x):
        resultado.append(corrida_x[i])
        i += 1
    while j < len(corrida_y):
        resultado.append(corrida_y[j])
        j += 1
    return resultado


def pasada_de_mezcla(entrada_1, entrada_2):
    """Una pasada: mezcla la corrida k de un archivo con la corrida k
    del otro y el resultado lo manda, alternando, a los dos archivos
    de salida."""
    salida_1 = []
    salida_2 = []
    total = max(len(entrada_1), len(entrada_2))

    for k in range(total):
        if k < len(entrada_1) and k < len(entrada_2):
            nueva = mezclar_corridas(entrada_1[k], entrada_2[k])
        elif k < len(entrada_1):
            nueva = entrada_1[k]  
        else:
            nueva = entrada_2[k]

        if k % 2 == 0:
            salida_1.append(nueva)
        else:
            salida_2.append(nueva)

    return salida_1, salida_2


def mezcla_equilibrada(datos, tamano_corrida):
    """Ordena la lista de datos con mezcla equilibrada."""
    corridas = crear_corridas(datos, tamano_corrida)
    print("Corridas iniciales (ya ordenadas por separado):")
    for corrida in corridas:
        print("  ", corrida)

    entrada_1, entrada_2 = repartir_corridas(corridas)
    print("\nReparto inicial:")
    print("  Archivo 1 =", entrada_1)
    print("  Archivo 2 =", entrada_2)

    pasada = 1
   
    while len(entrada_1) + len(entrada_2) > 1:
        salida_1, salida_2 = pasada_de_mezcla(entrada_1, entrada_2)
        print(f"\nPasada {pasada}:")
        print("  Archivo 3 =", salida_1)
        print("  Archivo 4 =", salida_2)

        
        entrada_1, entrada_2 = salida_1, salida_2
        pasada += 1

   
    if len(entrada_1) == 1:
        return entrada_1[0]
    return entrada_2[0]


if __name__ == "__main__":
    ventas = [1250, 830, 2100, 540, 1780, 960, 3020, 410, 1500, 2750,
              680, 1990, 350, 2400, 1120, 870, 2950, 1430, 590, 1860]

    print("Ventas del dia (sin orden):")
    print(ventas)
    print()

    resultado = mezcla_equilibrada(ventas, tamano_corrida=4)

    print("\nVentas ordenadas de menor a mayor:")
    print(resultado)