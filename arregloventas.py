class ArregloVentas:
    
    def __init__(self):
        self.meses = [
            "Enero", "Febrero", "Marzo", "Abril",
            "Mayo", "Junio", "Julio", "Agosto",
            "Septiembre", "Octubre", "Noviembre", "Diciembre"
        ]

        self.departamentos = [
            "Ropa", "Deportes", "Jugueteria"
        ]

        self.ventas = [[0] * 3 for i in range(12)]

    
    def insertar_venta(self, mes, departamento, cantidad):
        self.ventas[mes][departamento] = cantidad
        print("Venta registrada correctamente.")

    
    def buscar_venta(self, mes, departamento):
        print("Las ventas de", self.departamentos[departamento],
              "en", self.meses[mes], "son:",
              self.ventas[mes][departamento])

    
    def eliminar_venta(self, mes, departamento):
        self.ventas[mes][departamento] = 0
        print("Venta eliminada correctamente.")

    
    def mostrar_ventas(self):
        print("\nVENTAS MENSUALES")

        print(f"{'Mes':<15}{'Ropa':<12}{'Deportes':<12}{'Jugueteria':<12}")

        for i in range(12):
            print(f"{self.meses[i]:<15}"
                  f"{self.ventas[i][0]:<12}"
                  f"{self.ventas[i][1]:<12}"
                  f"{self.ventas[i][2]:<12}")

    
    def menu(self):
        opcion = 0

        while opcion != 5:
            print("\n--- MENU DE VENTAS ---")
            print("1. Insertar venta")
            print("2. Buscar venta")
            print("3. Eliminar venta")
            print("4. Mostrar ventas")
            print("5. Salir")

            opcion = int(input("Selecciona una opcion: "))

            if opcion >= 1 and opcion <= 3:
                print("\nSelecciona el mes:")

                for i in range(12):
                    print(i + 1, ".", self.meses[i])

                mes = int(input("Numero del mes: ")) - 1

                print("\nSelecciona el departamento:")
                print("1. Ropa")
                print("2. Deportes")
                print("3. Jugueteria")

                departamento = int(
                    input("Numero del departamento: ")
                ) - 1

                if mes >= 0 and mes < 12 and departamento >= 0 and departamento < 3:

                    if opcion == 1:
                        cantidad = int(
                            input("Ingresa la cantidad de ventas: ")
                        )

                        if cantidad >= 0:
                            self.insertar_venta(
                                mes, departamento, cantidad
                            )
                        else:
                            print("La cantidad no puede ser negativa.")

                    elif opcion == 2:
                        self.buscar_venta(mes, departamento)

                    elif opcion == 3:
                        self.eliminar_venta(mes, departamento)

                else:
                    print("El mes o departamento no es valido.")

            elif opcion == 4:
                self.mostrar_ventas()

            elif opcion == 5:
                print("Saliendo del programa...")

            else:
                print("Opcion no valida.")


programa = ArregloVentas()
programa.menu()