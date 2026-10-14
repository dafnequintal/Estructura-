"""
Torre de Hanoi JUGABLE (tkinter, viene incluido con Python)
Ejecutar:  python hanoi_juego.py

Como jugar:
  - Clic en una torre para levantar su disco superior.
  - Clic en otra torre para soltarlo (solo sobre un disco mas grande o torre vacia).
  - Tambien puedes arrastrar el disco con el mouse.
  - El deslizador cambia el numero de discos (1 a 8). Reset reinicia.
  - El boton "Medir tiempos" resuelve el problema con 5, 10, 30 y 64 discos
    y mide cuanto tarda (30 se puede ejecutar completo; 64 siempre se estima).
"""
import threading
import time
import tkinter as tk
from tkinter import messagebox

COLORES = ["#ef4444", "#f59e0b", "#eab308", "#22c55e",
           "#06b6d4", "#3b82f6", "#8b5cf6", "#ec4899"]
W, H = 840, 400
ZONA_W = 260
BASE_Y = H - 30
ALTO_DISCO = 28


class JuegoHanoi:
    def __init__(self, root):
        self.root = root
        root.title("Torre de Hanoi")
        root.configure(bg="#f4f6fb")

        # ----- barra superior -----
        barra = tk.Frame(root, bg="#f4f6fb")
        barra.pack(fill="x", padx=10, pady=8)
        tk.Button(barra, text="Reset", command=self.reiniciar).pack(side="left")
        self.escala = tk.Scale(barra, from_=1, to=8, orient="horizontal",
                               label="Discos", length=180, bg="#f4f6fb",
                               command=lambda v: self.reiniciar())
        self.escala.set(5)
        self.escala.pack(side="left", padx=15)
        self.lbl_mov = tk.Label(barra, font=("Arial", 12, "bold"), fg="#1d1dab",
                                bg="white", relief="solid", bd=2, padx=8, pady=4)
        self.lbl_mov.pack(side="left", padx=5)
        self.lbl_mejor = tk.Label(barra, font=("Arial", 12, "bold"), fg="#1d1dab",
                                  bg="white", relief="solid", bd=2, padx=8, pady=4)
        self.lbl_mejor.pack(side="left", padx=5)

       
        self.canvas = tk.Canvas(root, width=W, height=H, bg="#f4f6fb",
                                highlightthickness=0)
        self.canvas.pack(padx=10, pady=(0, 6))
        self.canvas.bind("<ButtonPress-1>", self.al_presionar)
        self.canvas.bind("<B1-Motion>", self.al_arrastrar)
        self.canvas.bind("<ButtonRelease-1>", self.al_soltar)

        self.lbl_msg = tk.Label(root, text="", font=("Arial", 12, "bold"),
                                bg="#f4f6fb")
        self.lbl_msg.pack(pady=(0, 8))

        self.reiniciar()

    
    def reiniciar(self):
        self.n = int(self.escala.get())
        self.torres = [list(range(self.n, 0, -1)), [], []]
        self.movs = 0
        self.origen = None      # torre seleccionada
        self.arrastrando = False
        self.pos = (0, 0)
        self.gano = False
        self.lbl_msg.config(text="", fg="black")
        self.dibujar()

    def torre_en(self, x):
        return max(0, min(2, int(x // (W / 3))))

    def mover(self, a, b):
        if a == b:
            return
        disco = self.torres[a][-1]
        if self.torres[b] and self.torres[b][-1] < disco:
            self.lbl_msg.config(text="⛔ No puedes poner un disco grande sobre uno pequeño",
                                fg="#dc2626")
            return
        self.torres[a].pop()
        self.torres[b].append(disco)
        self.movs += 1
        self.lbl_msg.config(text="", fg="black")
        if len(self.torres[2]) == self.n:
            self.gano = True
            minimo = 2 ** self.n - 1
            if self.movs == minimo:
                txt = f"🏆 ¡Perfecto! Mínimo posible: {self.movs} movimientos"
            else:
                txt = f"🎉 ¡Ganaste en {self.movs} movimientos! (mínimo: {minimo})"
            self.lbl_msg.config(text=txt, fg="#16a34a")

    
    def al_presionar(self, e):
        if self.gano:
            return
        i = self.torre_en(e.x)
        if self.origen is None:
            if self.torres[i]:
                self.origen = i
                self.arrastrando = False
                self.pos = (e.x, e.y)
        else:                      
            self.mover(self.origen, i)
            self.origen = None
        self.dibujar()

    def al_arrastrar(self, e):
        if self.origen is not None:
            self.arrastrando = True
            self.pos = (e.x, e.y)
            self.dibujar()

    def al_soltar(self, e):
        if self.origen is not None and self.arrastrando:
            self.mover(self.origen, self.torre_en(e.x))
            self.origen = None
            self.arrastrando = False
            self.dibujar()

    
    def ancho_disco(self, d):
        return 40 + d * (ZONA_W - 70) / 8

    def rect_disco(self, cx, y_base, d):
        w = self.ancho_disco(d)
        return cx - w / 2, y_base - ALTO_DISCO, cx + w / 2, y_base

    def dibujar(self):
        c = self.canvas
        c.delete("all")
        self.lbl_mov.config(text=f"{self.movs} movimiento" + ("" if self.movs == 1 else "s"))
        self.lbl_mejor.config(text=f"Mejor: {2 ** self.n - 1} movimientos")

        for i in range(3):
            x0 = i * (W / 3) + 10
            x1 = (i + 1) * (W / 3) - 10
            cx = (x0 + x1) / 2
            borde = "#ff9800" if self.origen == i else ""
            c.create_rectangle(x0, 40, x1, BASE_Y, fill="#e3efe6",
                               outline=borde, width=3)
            c.create_rectangle(cx - 6, 50, cx + 6, BASE_Y, fill="#8a5a00", outline="")
            c.create_text(cx, BASE_Y + 14, text="ABC"[i], font=("Arial", 11, "bold"),
                          fill="#555")
            for k, d in enumerate(self.torres[i]):
                # el disco levantado se dibuja aparte
                if self.origen == i and k == len(self.torres[i]) - 1:
                    continue
                y = BASE_Y - k * (ALTO_DISCO + 3)
                self.pintar(cx, y, d)

        c.create_rectangle(10, BASE_Y, W - 10, BASE_Y + 6, fill="#8a5a00", outline="")

        if self.origen is not None:
            d = self.torres[self.origen][-1]
            if self.arrastrando:
                cx, y = self.pos[0], self.pos[1] + ALTO_DISCO / 2
            else:
                cx = self.origen * (W / 3) + W / 6
                y = 75
            self.pintar(cx, y, d, sombra=True)

    def pintar(self, cx, y, d, sombra=False):
        x0, y0, x1, y1 = self.rect_disco(cx, y, d)
        if sombra:
            self.canvas.create_rectangle(x0 + 4, y0 + 6, x1 + 4, y1 + 6,
                                         fill="#999", outline="")
        self.canvas.create_rectangle(x0, y0, x1, y1, fill=COLORES[d - 1],
                                     outline="#222", width=3)

    
    def resolver_recursivo(self, n, origen, auxiliar, destino, torres, cont):
        """Resuelve con recursion moviendo discos de verdad. cont[0] = movimientos."""
        if n == 0:
            return
        self.resolver_recursivo(n - 1, origen, destino, auxiliar, torres, cont)
        torres[destino].append(torres[origen].pop())
        cont[0] += 1
        self.resolver_recursivo(n - 1, auxiliar, origen, destino, torres, cont)

    def resolver_medido(self, n):
        """Resuelve n discos y devuelve (movimientos, segundos)."""
        torres = [list(range(n, 0, -1)), [], []]
        cont = [0]
        ini = time.perf_counter()
        self.resolver_recursivo(n, 0, 1, 2, torres, cont)
        return cont[0], time.perf_counter() - ini

    @staticmethod
    def formatear_tiempo(seg):
        if seg < 60:
            return f"{seg:.6f} s"
        if seg < 3600:
            return f"{seg / 60:.2f} min"
        if seg < 86400:
            return f"{seg / 3600:.2f} horas"
        if seg < 31557600:
            return f"{seg / 86400:.2f} dias"
        return f"{seg / 31557600:.3e} anios"

    def estimar_tiempo(self, n, seg_por_mov):
        return (2 ** n - 1) * seg_por_mov

    def medir_tiempos(self):
        """Abre una ventana y lanza la medicion en un hilo (para no congelar el juego)."""
        if getattr(self, "midiendo", False):
            return
        self.midiendo = True
        self.ventana = tk.Toplevel(self.root)
        self.ventana.title("Medicion de tiempos")
        self.ventana.protocol("WM_DELETE_WINDOW", self.cerrar_medicion)
        self.completo30 = tk.BooleanVar(value=False)
        tk.Checkbutton(self.ventana, variable=self.completo30,
                       text="Ejecutar 30 discos completo (tarda varios minutos)"
                       ).pack(anchor="w", padx=10, pady=(8, 0))
        tk.Button(self.ventana, text="Iniciar",
                  command=self.iniciar_hilo).pack(pady=6)
        self.texto = tk.Text(self.ventana, width=78, height=14,
                             font=("Courier", 10), bg="#101426", fg="#e8eaff")
        self.texto.pack(padx=10, pady=(0, 10))
        for nombre, col in (("ok", "#22c55e"), ("est", "#f59e0b"),
                            ("info", "#06b6d4"), ("tit", "#ec4899")):
            self.texto.tag_config(nombre, foreground=col)
        self.escribir("Presiona Iniciar para medir 5, 10, 30 y 64 discos.\n", "info")

    def cerrar_medicion(self):
        self.midiendo = False
        self.ventana.destroy()

    def escribir(self, linea, tag=None):
        """Agrega una linea al cuadro de texto (se llama desde el hilo con after)."""
        self.texto.insert("end", linea, tag)
        self.texto.see("end")

    def iniciar_hilo(self):
        self.texto.delete("1.0", "end")
        hilo = threading.Thread(target=self.trabajo_medicion, daemon=True)
        hilo.start()

    def trabajo_medicion(self):
        def out(linea, tag=None):
            self.root.after(0, self.escribir, linea, tag)

        completo = self.completo30.get()
        out("=== BENCHMARK TORRE DE HANOI ===\n", "tit")
        movs, seg = self.resolver_medido(20)
        seg_mov = seg / movs
        out(f"Calibracion: 20 discos, {movs:,} mov en {seg:.3f} s "
            f"({seg_mov * 1e9:.0f} ns/mov)\n\n", "info")
        out(f"{'Discos':>6} | {'Movimientos':>26} | {'Tiempo':>16} | Tipo\n", "info")
        for n in (5, 10, 30, 64):
            total = 2 ** n - 1
            if n <= 10 or (n == 30 and completo):
                if n == 30:
                    out("Ejecutando 30 discos... espera unos minutos\n", "info")
                movs, seg = self.resolver_medido(n)
                tag, tipo = "ok", "medido"
            else:
                seg = self.estimar_tiempo(n, seg_mov)
                tag, tipo = "est", "ESTIMADO"
            out(f"{n:>6} | {total:>26,} | {self.formatear_tiempo(seg):>16} | {tipo}\n", tag)
        out("\nListo.\n", "tit")


if __name__ == "__main__":
    root = tk.Tk()
    JuegoHanoi(root)
    root.mainloop()
    