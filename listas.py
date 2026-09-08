class Vectores:
    
    def mostrar_vector(self, datos):
        for i in range(len(datos)):
            print(datos[i])
            
    def media(self, datos):
        n = len(datos)
        suma = 0
        
        for i in range(n):
            suma = suma + datos[i]
            
        return suma / n
    
vectores = Vectores()

pares = [2, 4, 6, 8, 10]
impares = [1, 3, 5, 7, 9]

vectores.mostrar_vector(pares)
print("Media =", vectores.media(pares))

vectores.mostrar_vector(impares)
print("Media =", vectores.media(impares))

        
            
