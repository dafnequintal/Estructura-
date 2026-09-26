import java.util.Scanner;

public class ArregloVentas {

    Scanner entrada = new Scanner(System.in);

    String[] meses = {
        "Enero", "Febrero", "Marzo", "Abril",
        "Mayo", "Junio", "Julio", "Agosto",
        "Septiembre", "Octubre", "Noviembre", "Diciembre"
    };

    String[] departamentos = {
        "Ropa", "Deportes", "Jugueteria"
    };

    int[][] ventas = new int[12][3];

    
    public void insertarVenta(int mes, int departamento, int cantidad) {
        ventas[mes][departamento] = cantidad;
        System.out.println("Venta registrada correctamente.");
    }

    
    public void buscarVenta(int mes, int departamento) {
        System.out.println("Las ventas de " + departamentos[departamento]
                + " en " + meses[mes] + " son: "
                + ventas[mes][departamento]);
    }

    
    public void eliminarVenta(int mes, int departamento) {
        ventas[mes][departamento] = 0;
        System.out.println("Venta eliminada correctamente.");
    }

   
    public void mostrarVentas() {
        System.out.println("\nVENTAS MENSUALES");

        System.out.printf("%-15s %-12s %-12s %-12s%n",
                "Mes", "Ropa", "Deportes", "Jugueteria");

        for (int i = 0; i < 12; i++) {
            System.out.printf("%-15s %-12d %-12d %-12d%n",
                    meses[i],
                    ventas[i][0],
                    ventas[i][1],
                    ventas[i][2]);
        }
    }

    
    public void menu() {
        int opcion;
        int mes;
        int departamento;
        int cantidad;

        do {
            System.out.println("\n--- MENU DE VENTAS ---");
            System.out.println("1. Insertar venta");
            System.out.println("2. Buscar venta");
            System.out.println("3. Eliminar venta");
            System.out.println("4. Mostrar ventas");
            System.out.println("5. Salir");
            System.out.print("Selecciona una opcion: ");
            opcion = entrada.nextInt();

            if (opcion >= 1 && opcion <= 3) {
                System.out.println("\nSelecciona el mes:");

                for (int i = 0; i < 12; i++) {
                    System.out.println((i + 1) + ". " + meses[i]);
                }

                System.out.print("Numero del mes: ");
                mes = entrada.nextInt() - 1;

                System.out.println("\nSelecciona el departamento:");
                System.out.println("1. Ropa");
                System.out.println("2. Deportes");
                System.out.println("3. Jugueteria");
                System.out.print("Numero del departamento: ");
                departamento = entrada.nextInt() - 1;

                if (mes >= 0 && mes < 12
                        && departamento >= 0 && departamento < 3) {

                    if (opcion == 1) {
                        System.out.print("Ingresa la cantidad de ventas: ");
                        cantidad = entrada.nextInt();

                        if (cantidad >= 0) {
                            insertarVenta(mes, departamento, cantidad);
                        } else {
                            System.out.println("La cantidad no puede ser negativa.");
                        }

                    } else if (opcion == 2) {
                        buscarVenta(mes, departamento);

                    } else if (opcion == 3) {
                        eliminarVenta(mes, departamento);
                    }

                } else {
                    System.out.println("El mes o departamento no es valido.");
                }

            } else if (opcion == 4) {
                mostrarVentas();

            } else if (opcion == 5) {
                System.out.println("Saliendo del programa...");

            } else {
                System.out.println("Opcion no valida.");
            }

        } while (opcion != 5);
    }

    public static void main(String[] args) {
        ArregloVentas programa = new ArregloVentas();
        programa.menu();
    }
}