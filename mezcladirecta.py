"""
Ejercicio 2: Mezcla directa
Materia: Estructura de Datos
Alumna: Dafne Andrea Quintal Medina

Problema: el almacen de una tienda tiene un archivo con los codigos de
sus productos capturados sin orden. Si el archivo fuera muy grande no
cabria completo en memoria, asi que se ordena usando archivos
auxiliares. Aqui los archivos se simulan con listas de Python.
"""


def distribuir(archivo_a, longitud):
    """Reparte los datos de A en B y C, alternando bloques del
    tamano 'longitud' (primer bloque a B, segundo a C, y asi)."""
    archivo_b = []
    archivo_c = []
    numero_bloque = 0
    for inicio in range(0, len(archivo_a), longitud):
        bloque = archivo_a[inicio:inicio + longitud]
        if numero_bloque % 2 == 0:
            archivo_b.extend(bloque)
        else:
            archivo_c.extend(bloque)
        numero_bloque += 1
    return archivo_b, archivo_c


def mezclar(archivo_b, archivo_c, longitud):
    """Toma un bloque de B y un bloque de C, los mezcla ordenados y
    los escribe en A. Repite hasta terminar los dos archivos."""
    archivo_a = []
    pos_b = 0
    pos_c = 0

    while pos_b < len(archivo_b) or pos_c < len(archivo_c):
        # Donde termina el bloque actual de cada archivo
        fin_b = min(pos_b + longitud, len(archivo_b))
        fin_c = min(pos_c + longitud, len(archivo_c))

        
        while pos_b < fin_b and pos_c < fin_c:
            if archivo_b[pos_b] <= archivo_c[pos_c]:
                archivo_a.append(archivo_b[pos_b])
                pos_b += 1
            else:
                archivo_a.append(archivo_c[pos_c])
                pos_c += 1

        
        while pos_b < fin_b:
            archivo_a.append(archivo_b[pos_b])
            pos_b += 1
        while pos_c < fin_c:
            archivo_a.append(archivo_c[pos_c])
            pos_c += 1

    return archivo_a


def mezcla_directa(archivo_a):
    """Ordena el archivo A de menor a mayor con mezcla directa."""
    longitud = 1  
    pasada = 1
    while longitud < len(archivo_a):
        archivo_b, archivo_c = distribuir(archivo_a, longitud)
        archivo_a = mezclar(archivo_b, archivo_c, longitud)

        print(f"Pasada {pasada} (bloques de {longitud}):")
        print("  B =", archivo_b)
        print("  C =", archivo_c)
        print("  A =", archivo_a)

        longitud = longitud * 2  
        pasada += 1
    return archivo_a


if __name__ == "__main__":
    codigos = [45, 12, 78, 33, 5, 91, 27, 60, 18, 84, 39, 52]

    print("Codigos capturados (sin orden):")
    print(codigos)
    print()

    ordenados = mezcla_directa(codigos)

    print("\nCodigos ordenados:")
    print(ordenados)