"""
Simulador gráfico de una PILA (Stack) - estructura LIFO
(Last In, First Out: el último en entrar es el primero en salir)

Solo usa tkinter, que ya viene incluido con Python.
Ejecutar:  python pila_grafica.py
"""

import tkinter as tk
from tkinter import messagebox


CAPACIDAD = 8         
ALTO_BLOQUE = 45      
X1, X2 = 230, 470      
BASE = 500             
Y_ENTRADA = 70         
COLORES = ["#6F8FBF", "#B5E61D", "#EFE4B0", "#F4A8A8", "#B8A9E8", "#8FD9C4", "#FFC87A", "#9ED2F0"]


class PilaGrafica:
    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.title("Pila de datos - Simulador gráfico")
        self.ventana.resizable(False, False)

        self.pila = []          
        self.animando = False   

        self._crear_widgets()
        self._dibujar_escenario()
        self._actualizar_estado()

    
    def _crear_widgets(self):
        self.canvas = tk.Canvas(self.ventana, width=700, height=540, bg="white", highlightthickness=0)
        self.canvas.pack()

        panel = tk.Frame(self.ventana, pady=8)
        panel.pack()

        tk.Label(panel, text="Dato:", font=("Arial", 11)).grid(row=0, column=0, padx=4)
        self.entrada = tk.Entry(panel, width=14, font=("Arial", 12))
        self.entrada.grid(row=0, column=1, padx=4)
        self.entrada.bind("<Return>", lambda e: self.apilar())
        self.entrada.focus()

        estilo = {"font": ("Arial", 10, "bold"), "width": 11, "fg": "white"}
        tk.Button(panel, text="Apilar", bg="#2E8B57", command=self.apilar, **estilo).grid(row=0, column=2, padx=4)
        tk.Button(panel, text="Desapilar", bg="#C0392B", command=self.desapilar, **estilo).grid(row=0, column=3, padx=4)
        tk.Button(panel, text="Ver tope", bg="#2980B9", command=self.ver_tope, **estilo).grid(row=0, column=4, padx=4)
        tk.Button(panel, text="Vaciar", bg="#7F8C8D", command=self.vaciar, **estilo).grid(row=0, column=5, padx=4)

        self.lbl_estado = tk.Label(self.ventana, text="", font=("Arial", 11), pady=6)
        self.lbl_estado.pack()

    def _dibujar_escenario(self):
        c = self.canvas
        rojo = "red"

       
        c.create_text(350, 30, text="PILA DE DATOS", fill=rojo, font=("Arial", 16, "bold"))

       
        c.create_line(X1, 120, X1, BASE + 5, width=5)
        c.create_line(X1, BASE + 5, X2, BASE + 5, width=5)
        c.create_line(X2, 120, X2, BASE + 5, width=5)

      
        c.create_text(95, 105, text="Apilar", fill=rojo, font=("Arial", 14, "bold"))
        c.create_line(70, 130, X1 + 40, 130, X1 + 40, 175, width=4, arrow=tk.LAST, arrowshape=(14, 16, 6))

        # Flecha y texto de DESAPILAR (sale por la derecha)
        c.create_text(X2 + 95, 105, text="Desapilar", fill=rojo, font=("Arial", 14, "bold"))
        c.create_line(X2 - 40, 175, X2 - 40, 130, X2 + 150, 130, width=4, arrow=tk.LAST, arrowshape=(14, 16, 6))

        
        c.create_text(X2 + 15, BASE - 12, text="Fondo de la pila", anchor="w",
                      fill=rojo, font=("Arial", 12, "bold"))

    
    def apilar(self):
        """PUSH: agrega un dato en el tope de la pila."""
        if self.animando:
            return
        dato = self.entrada.get().strip()
        if not dato:
            messagebox.showwarning("Dato vacío", "Escribe un dato para apilar.")
            return
        if len(self.pila) >= CAPACIDAD:
            messagebox.showerror("Pila llena", "Desbordamiento de pila (Stack Overflow):\n"
                                               "no se pueden apilar más datos.")
            return

        self.entrada.delete(0, tk.END)
        nivel = len(self.pila)
        y_destino = BASE - (nivel + 1) * ALTO_BLOQUE
        color = COLORES[nivel % len(COLORES)]

        rect = self.canvas.create_rectangle(X1 + 3, Y_ENTRADA, X2 - 3, Y_ENTRADA + ALTO_BLOQUE,
                                            fill=color, outline="white", width=2)
        texto = self.canvas.create_text((X1 + X2) / 2, Y_ENTRADA + ALTO_BLOQUE / 2,
                                        text=dato, font=("Arial", 13, "bold"))
        self.canvas.delete("tope")
        self.animando = True
        self._animar_bajada(dato, rect, texto, Y_ENTRADA, y_destino)

    def _animar_bajada(self, dato, rect, texto, y_actual, y_destino):
        if y_actual < y_destino:
            paso = min(10, y_destino - y_actual)
            self.canvas.move(rect, 0, paso)
            self.canvas.move(texto, 0, paso)
            self.ventana.after(15, self._animar_bajada, dato, rect, texto, y_actual + paso, y_destino)
        else:
            self.pila.append((dato, rect, texto))
            self.animando = False
            self._actualizar_estado(f"Se apiló: {dato}")

    def desapilar(self):
        """POP: saca y elimina el dato que está en el tope."""
        if self.animando:
            return
        if not self.pila:
            messagebox.showerror("Pila vacía", "Subdesbordamiento de pila (Stack Underflow):\n"
                                               "no hay datos para desapilar.")
            return

        dato, rect, texto = self.pila.pop()
        self.canvas.delete("tope")
        self.animando = True
        y_actual = self.canvas.coords(rect)[1]
        self._animar_subida(dato, rect, texto, y_actual)

    def _animar_subida(self, dato, rect, texto, y_actual):
        if y_actual > Y_ENTRADA:
            paso = min(10, y_actual - Y_ENTRADA)
            self.canvas.move(rect, 0, -paso)
            self.canvas.move(texto, 0, -paso)
            self.ventana.after(15, self._animar_subida, dato, rect, texto, y_actual - paso)
        else:
            self.canvas.delete(rect)
            self.canvas.delete(texto)
            self.animando = False
            self._actualizar_estado(f"Se desapiló: {dato}")

    def ver_tope(self):
        """PEEK: muestra el dato del tope sin eliminarlo."""
        if self.animando:
            return
        if not self.pila:
            messagebox.showinfo("Tope", "La pila está vacía.")
        else:
            messagebox.showinfo("Tope", f"El dato en el tope es: {self.pila[-1][0]}")

    def vaciar(self):
        if self.animando:
            return
        for _, rect, texto in self.pila:
            self.canvas.delete(rect)
            self.canvas.delete(texto)
        self.pila.clear()
        self._actualizar_estado("La pila fue vaciada")


    def _actualizar_estado(self, mensaje=""):
        self.canvas.delete("tope")
        if self.pila:
            y_centro = BASE - len(self.pila) * ALTO_BLOQUE + ALTO_BLOQUE / 2
            self.canvas.create_text(X2 + 15, y_centro, text="◄ Tope de la pila", anchor="w",
                                    fill="red", font=("Arial", 12, "bold"), tags="tope")
        else:
            self.canvas.create_text((X1 + X2) / 2, BASE - 60, text="(Pila vacía)",
                                    fill="gray", font=("Arial", 12, "italic"), tags="tope")

        situacion = "VACÍA" if not self.pila else ("LLENA" if len(self.pila) == CAPACIDAD else "con datos")
        tope = self.pila[-1][0] if self.pila else "—"
        self.lbl_estado.config(
            text=f"{mensaje}   |   Elementos: {len(self.pila)}/{CAPACIDAD}   |   Tope: {tope}   |   Estado: {situacion}"
        )


if __name__ == "__main__":
    root = tk.Tk()
    PilaGrafica(root)
    root.mainloop()