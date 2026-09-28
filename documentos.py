import os

def contar_archivos(carpeta):
    cantidad = 0

    for elemento in os.listdir(carpeta):
        ruta = os.path.join(carpeta, elemento)

        if os.path.isfile(ruta):
            cantidad += 1
#R
        elif os.path.isdir(ruta):
            cantidad += contar_archivos(ruta)

    return cantidad



carpeta = input("Escribe la ruta de la carpeta: ")

if os.path.exists(carpeta):
    total = contar_archivos(carpeta)
    print("Cantidad total de archivos:", total)
else:
    print("La carpeta no existe.")