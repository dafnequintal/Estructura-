import random
import statistics


class Vectores:

    def mostrar_vector(self, datos):
        for i in range(len(datos)):
            print(datos[i])

    def media(self, datos):
        return statistics.mean(datos)

    def mediana(self, datos):
        return statistics.median(datos)

    def moda(self, datos):
        return statistics.mode(datos)

    def varianza(self, datos):
        return statistics.pvariance(datos)

    def desviacion_estandar(self, datos):
        return statistics.pstdev(datos)


# Programa principal

vectores = Vectores()

# Generar una lista de 50 números enteros entre 1 y 100
datos = [random.randint(150, 250) for i in range(50)]

print("Lista de 50 números:")
vectores.mostrar_vector(datos)

print("\nMedia =", vectores.media(datos))
print("Mediana =", vectores.mediana(datos))
print("Moda =", vectores.moda(datos))
print("Varianza =", vectores.varianza(datos))
print("Desviación estándar =", vectores.desviacion_estandar(datos))
