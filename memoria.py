class Memoria:
    
    def memoria_estatica(self):
        calificaciones = [0] * 5

        for i in range(5):
            calificaciones[i] = int(input("Captura la calificación: "))

        print(calificaciones)

    def memoria_dinamica(self):
        frutas = []

        frutas.append("Mango")
        frutas.append("Manzana")
        frutas.append("Banana")
        frutas.append("Uvas")

        print(frutas)

        frutas.remove("Mango")
        frutas.remove("Banana")

        frutas.append("Sandia")

        print(frutas)


programa = Memoria()
programa.memoria_estatica()
programa.memoria_dinamica()